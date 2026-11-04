#!/usr/bin/env python3
"""distiller.py - Deterministyczna destylacja transkryptów sesji (Code Over AI).

Redukuje rozmiar transkryptów o 95-99%, usuwa szum wywołań narzędzi,
maskuje sekrety i zachowuje wyłącznie sygnał decyzyjny (pytanie, próba, błąd, korekta).
"""

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DistilledSession:
    session_id: str
    harness: str
    file_path: str
    created_at: str
    original_size_bytes: int
    distilled_size_bytes: int
    compression_ratio: float
    turns: List[Dict[str, str]]
    compact_text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


SECRET_PATTERNS = [
    (r"sk-[a-zA-Z0-9_-]{20,}", "[REDACTED_API_KEY]"),
    (r"ghp_[a-zA-Z0-9]{20,}", "[REDACTED_GITHUB_TOKEN]"),
    (r"anthropic-[a-zA-Z0-9_-]{20,}", "[REDACTED_ANTHROPIC_KEY]"),
    (r"AIza[0-9A-Za-z-_]{35}", "[REDACTED_GOOGLE_KEY]"),
    (r"eyJ[a-zA-Z0-9_-]{15,}\.[a-zA-Z0-9_-]{15,}\.[a-zA-Z0-9_-]{10,}", "[REDACTED_JWT]"),
    (r"(?i)(password|passwd|token|secret|api_key|apikey)\s*[:=]\s*['\"][^'\"]{6,}['\"]", r'\1: "[REDACTED]"'),
]


def redact_secrets(text: str) -> str:
    """Maskuje klucze API, hasła i tokeny w tekście."""
    if not text:
        return ""
    result = text
    for pattern, replacement in SECRET_PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result


def truncate_snippet(text: str, max_chars: int = 250) -> str:
    """Skraca długi tekst do zwięzłego podglądu jednej lub dwóch linii."""
    if not text:
        return ""
    clean = " ".join(text.strip().split())
    if len(clean) <= max_chars:
        return clean
    return clean[:max_chars] + "..."


def distill_antigravity_transcript(file_path: Path, session_id: str) -> DistilledSession:
    """Destyluje transkrypt Antigravity JSONL."""
    orig_size = file_path.stat().st_size
    turns: List[Dict[str, str]] = []
    created_at = ""

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except Exception:
                    continue

                if not created_at and "created_at" in item:
                    created_at = item["created_at"]

                source = item.get("source", "")
                step_type = item.get("type", "")
                content = item.get("content", "")
                status = item.get("status", "")
                tool_calls = item.get("tool_calls", [])

                # Pytanie lub odpowiedź użytkownika
                if step_type == "USER_INPUT" or source == "USER_EXPLICIT":
                    clean_content = redact_secrets(content.strip())
                    if clean_content:
                        turns.append({"role": "user", "text": clean_content})

                # Odpowiedź / myślenie modelu
                elif step_type == "PLANNER_RESPONSE" or source == "MODEL":
                    clean_resp = redact_secrets(content.strip()) if content else ""
                    # Jeśli były wywołania narzędzi, dopisujemy ich podsumowanie
                    tool_summaries = []
                    for tc in tool_calls:
                        t_name = tc.get("name") or tc.get("toolName") or "tool"
                        args = tc.get("args") or tc.get("arguments") or {}
                        # Ekstrakcja kluczowych argumentów
                        arg_parts = []
                        for k in ("CommandLine", "AbsolutePath", "TargetFile", "Query", "Url", "Pattern"):
                            if k in args:
                                arg_parts.append(f"{k}={truncate_snippet(str(args[k]), 80)}")
                        arg_str = ", ".join(arg_parts) if arg_parts else truncate_snippet(json.dumps(args), 80)
                        tool_summaries.append(f"ToolCall: {t_name}({arg_str})")

                    entry_text = []
                    if clean_resp:
                        entry_text.append(truncate_snippet(clean_resp, 350))
                    if tool_summaries:
                        entry_text.extend(tool_summaries)

                    if entry_text:
                        turns.append({"role": "assistant", "text": "\n".join(entry_text)})

                # Wyniki narzędzi - rejestrujemy tylko status i ewentualny błąd
                elif step_type in ("RUN_COMMAND", "VIEW_FILE", "EDIT_FILE", "CALL_MCP_TOOL"):
                    if status == "ERROR" or (content and "error" in content.lower()[:200]):
                        err_snip = truncate_snippet(redact_secrets(content), 200)
                        turns.append({"role": "tool_result", "text": f"[Status: {status}] {err_snip}"})
    except Exception as e:
        turns.append({"role": "error", "text": f"Błąd odczytu pliku: {e}"})

    # Składamy kompaktowy tekst
    lines = [f"=== SESSION {session_id} (Harness: Antigravity, Date: {created_at[:10] if created_at else 'Unknown'}) ==="]
    for t in turns:
        role = t["role"].upper()
        lines.append(f"[{role}]: {t['text']}")
    compact_text = "\n".join(lines)
    dist_size = len(compact_text.encode("utf-8"))
    ratio = round(dist_size / max(orig_size, 1), 4)

    return DistilledSession(
        session_id=session_id,
        harness="antigravity",
        file_path=str(file_path),
        created_at=created_at,
        original_size_bytes=orig_size,
        distilled_size_bytes=dist_size,
        compression_ratio=ratio,
        turns=turns,
        compact_text=compact_text,
    )


def distill_claude_transcript(file_path: Path, session_id: str) -> DistilledSession:
    """Destyluje transkrypt Claude Code JSONL."""
    orig_size = file_path.stat().st_size
    turns: List[Dict[str, str]] = []
    created_at = ""

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except Exception:
                    continue

                if not created_at and "timestamp" in item:
                    created_at = item["timestamp"]

                m_type = item.get("type", "")
                if m_type == "user" or "user_message" in item:
                    msg = item.get("message") or item.get("content") or item.get("user_message") or ""
                    clean_msg = redact_secrets(str(msg).strip())
                    if clean_msg:
                        turns.append({"role": "user", "text": clean_msg})

                elif m_type == "assistant" or "assistant_message" in item:
                    msg = item.get("message") or item.get("content") or item.get("assistant_message") or ""
                    clean_msg = redact_secrets(str(msg).strip())
                    if clean_msg:
                        turns.append({"role": "assistant", "text": truncate_snippet(clean_msg, 350)})

                elif m_type == "tool_use":
                    tool_name = item.get("name", "tool")
                    args = item.get("input", {})
                    turns.append({"role": "assistant", "text": f"ToolCall: {tool_name}({truncate_snippet(json.dumps(args), 100)})"})

                elif m_type == "tool_result" and (item.get("is_error") or "error" in str(item.get("content", "")).lower()[:100]):
                    turns.append({"role": "tool_result", "text": f"[Error] {truncate_snippet(redact_secrets(str(item.get('content', ''))), 200)}"})
    except Exception as e:
        turns.append({"role": "error", "text": f"Błąd odczytu pliku: {e}"})

    lines = [f"=== SESSION {session_id} (Harness: Claude Code, Date: {created_at[:10] if created_at else 'Unknown'}) ==="]
    for t in turns:
        lines.append(f"[{t['role'].upper()}]: {t['text']}")
    compact_text = "\n".join(lines)
    dist_size = len(compact_text.encode("utf-8"))
    ratio = round(dist_size / max(orig_size, 1), 4)

    return DistilledSession(
        session_id=session_id,
        harness="claude",
        file_path=str(file_path),
        created_at=created_at,
        original_size_bytes=orig_size,
        distilled_size_bytes=dist_size,
        compression_ratio=ratio,
        turns=turns,
        compact_text=compact_text,
    )


def distill_markdown_transcript(file_path: Path, session_id: str, harness: str = "markdown_brudnopis") -> DistilledSession:
    """Destyluje transkrypt lub wpis dziennika w Markdown."""
    orig_size = file_path.stat().st_size
    turns: List[Dict[str, str]] = []
    created_at = ""

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        clean_content = redact_secrets(content)

        # Wyciągamy nagłówki, wnioski, problemy, zadania
        sections = []
        current_section = []
        for line in clean_content.splitlines():
            if line.startswith("#"):
                if current_section:
                    sections.append("\n".join(current_section))
                    current_section = []
            current_section.append(line)
        if current_section:
            sections.append("\n".join(current_section))

        for sec in sections:
            sec_clean = truncate_snippet(sec, 500)
            if sec_clean:
                turns.append({"role": "doc_section", "text": sec_clean})
    except Exception as e:
        turns.append({"role": "error", "text": f"Błąd odczytu pliku: {e}"})

    lines = [f"=== SESSION {session_id} (Harness: {harness}) ==="]
    for t in turns:
        lines.append(f"[{t['role'].upper()}]: {t['text']}")
    compact_text = "\n".join(lines)
    dist_size = len(compact_text.encode("utf-8"))
    ratio = round(dist_size / max(orig_size, 1), 4)

    return DistilledSession(
        session_id=session_id,
        harness=harness,
        file_path=str(file_path),
        created_at=created_at,
        original_size_bytes=orig_size,
        distilled_size_bytes=dist_size,
        compression_ratio=ratio,
        turns=turns,
        compact_text=compact_text,
    )


def distill_session(file_path: str, harness: str, session_id: str) -> DistilledSession:
    """Uniwersalny dyspozytor destylacji sesji."""
    p = Path(file_path)
    if harness == "antigravity":
        return distill_antigravity_transcript(p, session_id)
    elif harness == "claude":
        return distill_claude_transcript(p, session_id)
    else:
        return distill_markdown_transcript(p, session_id, harness)


if __name__ == "__main__":
    import sys
    from scanner import scan_all_sessions

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sessions = scan_all_sessions(target, since="7d", max_sessions=3)
    for s in sessions:
        d = distill_session(s.file_path, s.harness, s.session_id)
        print(f"\n--- Zdestylowano {d.session_id} [{d.harness}] ---")
        print(f"Oryginał: {d.original_size_bytes}B -> Destylat: {d.distilled_size_bytes}B (Kompresja: {d.compression_ratio*100:.1f}%)")
        print(f"Liczba tur: {len(d.turns)}")
        print("Próbka tekstu:")
        print(d.compact_text[:300] + "...")
