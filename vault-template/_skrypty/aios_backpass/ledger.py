#!/usr/bin/env python3
"""ledger.py - Deterministyczny rejestr luk i dowodów (Gap Ledger).

Zarządza bazą gap-ledger.json, wymuszając zasadę gradient descent:
żadna nowa reguła nie może powstać na podstawie jednej anegdotycznej sesji.
Wymaga potwierdzenia z co najmniej 2 niezależnych sesji (min_sessions >= 2).
"""

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class EvidenceQuote:
    session_id: str
    harness: str
    date: str
    quote: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GapRecord:
    gap_id: str
    title: str
    category: str  # rule_violation | missing_rule | stale_rule | unneeded_discovery
    affected_section: str
    first_seen: str
    last_seen: str
    sessions_count: int
    evidence_quotes: List[EvidenceQuote]
    status: str = "unconfirmed"  # unconfirmed | graduated | converted_to_rule | extracted_to_skill | rejected
    rejection_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gap_id": self.gap_id,
            "title": self.title,
            "category": self.category,
            "affected_section": self.affected_section,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "sessions_count": self.sessions_count,
            "evidence_quotes": [eq.to_dict() for eq in self.evidence_quotes],
            "status": self.status,
            "rejection_reason": self.rejection_reason,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GapRecord":
        quotes = [
            EvidenceQuote(
                session_id=q["session_id"],
                harness=q.get("harness", "unknown"),
                date=q.get("date", ""),
                quote=q["quote"],
            )
            for q in data.get("evidence_quotes", [])
        ]
        return cls(
            gap_id=data["gap_id"],
            title=data["title"],
            category=data.get("category", "missing_rule"),
            affected_section=data.get("affected_section", "Ogólne"),
            first_seen=data.get("first_seen", ""),
            last_seen=data.get("last_seen", ""),
            sessions_count=data.get("sessions_count", len(quotes)),
            evidence_quotes=quotes,
            status=data.get("status", "unconfirmed"),
            rejection_reason=data.get("rejection_reason"),
        )


class GapLedger:
    """Zarządza plikiem gap-ledger.json."""

    def __init__(self, ledger_path: Optional[Path] = None):
        self.ledger_path = ledger_path or Path.cwd() / ".aios-loop" / "gap-ledger.json"
        self.gaps: Dict[str, GapRecord] = {}
        self.load()

    def load(self) -> None:
        """Wczytuje stan rejestru z dysku."""
        if not self.ledger_path.exists():
            self.gaps = {}
            return

        try:
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            gaps_data = data.get("gaps", {})
            self.gaps = {gid: GapRecord.from_dict(gdata) for gid, gdata in gaps_data.items()}
        except Exception as e:
            print(f"[GapLedger] Ostrzeżenie: Błąd wczytywania ledger {self.ledger_path}: {e}")
            self.gaps = {}

    def save(self) -> None:
        """Zapisuje stan rejestru na dysk."""
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "1.0",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_gaps": len(self.gaps),
            "graduated_count": len([g for g in self.gaps.values() if g.status == "graduated"]),
            "gaps": {gid: g.to_dict() for gid, g in self.gaps.items()},
        }
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    @staticmethod
    def generate_gap_id(title: str, category: str) -> str:
        """Generuje stabilny ID luki na podstawie znormalizowanego tytułu i kategorii."""
        norm = f"{category.strip().lower()}:{title.strip().lower()}"
        slug = re.sub(r"[^a-z0-9]+", "-", title.strip().lower())[:30].strip("-")
        h = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:6]
        return f"{slug}-{h}" if slug else f"gap-{h}"

    def record_evidence(
        self,
        title: str,
        category: str,
        affected_section: str,
        session_id: str,
        harness: str,
        quote: str,
        min_sessions: int = 2,
        date_str: Optional[str] = None,
    ) -> GapRecord:
        """Rejestruje dowód błędu/luki z danej sesji."""
        gap_id = self.generate_gap_id(title, category)
        now_iso = date_str or datetime.now(timezone.utc).isoformat()

        if gap_id not in self.gaps:
            eq = EvidenceQuote(session_id=session_id, harness=harness, date=now_iso, quote=quote)
            record = GapRecord(
                gap_id=gap_id,
                title=title,
                category=category,
                affected_section=affected_section,
                first_seen=now_iso,
                last_seen=now_iso,
                sessions_count=1,
                evidence_quotes=[eq],
                status="graduated" if min_sessions <= 1 else "unconfirmed",
            )
            self.gaps[gap_id] = record
        else:
            record = self.gaps[gap_id]
            existing_sess = {eq.session_id for eq in record.evidence_quotes}
            if session_id not in existing_sess:
                record.evidence_quotes.append(
                    EvidenceQuote(session_id=session_id, harness=harness, date=now_iso, quote=quote)
                )
                record.sessions_count = len(record.evidence_quotes)
                record.last_seen = now_iso

            if record.status in ("unconfirmed", "graduated"):
                if record.sessions_count >= min_sessions:
                    record.status = "graduated"
                else:
                    record.status = "unconfirmed"

        return record

    def get_graduated_gaps(self) -> List[GapRecord]:
        """Zwraca luki gotowe do wdrożenia jako reguła (przeszły próg sesji)."""
        return [g for g in self.gaps.values() if g.status == "graduated"]

    def get_unconfirmed_gaps(self) -> List[GapRecord]:
        """Zwraca luki czekające na drugie potwierdzenie."""
        return [g for g in self.gaps.values() if g.status == "unconfirmed"]

    def mark_status(self, gap_id: str, new_status: str, reason: Optional[str] = None) -> bool:
        """Zmienia status luki (np. converted_to_rule, rejected)."""
        if gap_id not in self.gaps:
            return False
        rec = self.gaps[gap_id]
        rec.status = new_status
        if reason:
            rec.rejection_reason = reason
        self.save()
        return True

    def clean_expired(self, max_age_days: int = 90) -> int:
        """Usuwa niepotwierdzone luki starsze niż limit dni."""
        now_ts = datetime.now(timezone.utc).timestamp()
        cutoff_sec = max_age_days * 86400.0
        removed = 0
        to_delete = []

        for gid, g in self.gaps.items():
            if g.status == "unconfirmed":
                try:
                    dt = datetime.fromisoformat(g.last_seen)
                    if (now_ts - dt.timestamp()) > cutoff_sec:
                        to_delete.append(gid)
                except Exception:
                    pass

        for gid in to_delete:
            del self.gaps[gid]
            removed += 1

        if removed:
            self.save()
        return removed


if __name__ == "__main__":
    ledger = GapLedger()
    print(f"Załadowano ledger: {len(ledger.gaps)} luk.")
