#!/usr/bin/env python3
"""scanner.py – Wielo-środowiskowy skaner transkryptów sesji agentów.

Wyszukuje i mapuje sesje z różnych runtime'ów (Antigravity, Claude Code, Codex,
OpenCode, Cursor oraz plików markdown w _brudnopis/ i _pamiec/dziennik/).
"""

import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SessionMeta:
    session_id: str
    harness: str
    file_path: str
    created_at: str
    mtime: float
    cwd: Optional[str] = None
    project_name: Optional[str] = None
    size_bytes: int = 0
    turns_count: int = 0
    match_tier: int = 1  # 1: ścisłe dopasowanie ścieżki, 2: git/projekt, 3: heurystyka

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def parse_duration_to_seconds(duration_str: str) -> float:
    """Konwertuje ciąg np. '7d', '24h', '30m' na sekundy."""
    if not duration_str:
        return 7 * 86400.0  # domyślnie 7 dni
    
    match = re.match(r"^(\d+(?:\.\d+)?)\s*([smhdw]?)$", duration_str.strip().lower())
    if not match:
        return 7 * 86400.0
    
    val, unit = float(match.group(1)), match.group(2)
    multipliers = {
        's': 1.0,
        'm': 60.0,
        'h': 3600.0,
        'd': 86400.0,
        'w': 7 * 86400.0,
        '': 86400.0,
    }
    return val * multipliers.get(unit, 86400.0)


def is_path_related(candidate_cwd: Optional[str], target_path: Path) -> bool:
    """Sprawdza czy katalog sesji jest tożsamy lub leży wewnątrz docelowego projektu."""
    if not candidate_cwd:
        return False
    try:
        cand = Path(candidate_cwd).resolve()
        targ = target_path.resolve()
        # Tożsamy lub jeden zawiera drugi
        return cand == targ or targ in cand.parents or cand in targ.parents
    except Exception:
        return False


def scan_antigravity_sessions(
    target_path: Path,
    min_mtime: float,
    max_count: int = 100
) -> List[SessionMeta]:
    """Skanuje sesje Antigravity w ~/.gemini/antigravity/brain/."""
    brain_dir = Path.home() / ".gemini" / "antigravity" / "brain"
    if not brain_dir.exists():
        return []

    sessions: List[SessionMeta] = []
    target_resolved = target_path.resolve()
    target_name = target_resolved.name.lower()

    for entry in brain_dir.iterdir():
        if not entry.is_dir() or entry.name.startswith("."):
            continue

        # Transkrypty Antigravity mogą leżeć bezpośrednio lub w .system_generated/logs/
        t_paths = [
            entry / ".system_generated" / "logs" / "transcript.jsonl",
            entry / "transcript.jsonl",
        ]
        t_file = next((p for p in t_paths if p.exists()), None)
        if not t_file:
            continue

        st = t_file.stat()
        if st.st_mtime < min_mtime:
            continue

        # Próbujemy odczytać metadane i sprawdzić powiązanie z repozytorium
        turns = 0
        related = False
        detected_cwd = None
        match_tier = 3
        first_created = None

        try:
            with open(t_file, "r", encoding="utf-8", errors="ignore") as f:
                for line_idx, line in enumerate(f):
                    if not line.strip():
                        continue
                    turns += 1
                    if line_idx > 100 and related:
                        # Wystarczy potwierdzenie z początku sesji
                        continue
                    
                    try:
                        step = json.loads(line)
                        if not first_created and "created_at" in step:
                            first_created = step["created_at"]
                        
                        # Sprawdzamy CWD z wywołań narzędzi lub zawartości
                        content_str = str(step.get("content", ""))
                        tool_calls = step.get("tool_calls", [])
                        
                        if str(target_resolved) in content_str or target_name in content_str.lower():
                            related = True
                            match_tier = 1
                            detected_cwd = str(target_resolved)
                            
                        for tc in tool_calls:
                            args = tc.get("args") or tc.get("arguments") or {}
                            cwd_arg = args.get("Cwd") or args.get("cwd") or args.get("SearchDirectory") or args.get("DirectoryPath")
                            if cwd_arg:
                                detected_cwd = str(cwd_arg)
                                if is_path_related(cwd_arg, target_resolved):
                                    related = True
                                    match_tier = 1
                                    break
                    except Exception:
                        pass
        except Exception:
            continue

        if related or is_path_related(detected_cwd, target_resolved):
            dt_str = first_created or datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat()
            sessions.append(
                SessionMeta(
                    session_id=entry.name,
                    harness="antigravity",
                    file_path=str(t_file),
                    created_at=dt_str,
                    mtime=st.st_mtime,
                    cwd=detected_cwd or str(target_resolved),
                    project_name=target_name,
                    size_bytes=st.st_size,
                    turns_count=turns,
                    match_tier=match_tier,
                )
            )

    return sorted(sessions, key=lambda s: s.mtime, reverse=True)[:max_count]


def scan_claude_sessions(
    target_path: Path,
    min_mtime: float,
    max_count: int = 100
) -> List[SessionMeta]:
    """Skanuje sesje Claude Code w ~/.claude/projects/."""
    claude_dir = Path.home() / ".claude" / "projects"
    if not claude_dir.exists():
        return []

    sessions: List[SessionMeta] = []
    target_resolved = target_path.resolve()
    target_name = target_resolved.name.lower()

    for proj_dir in claude_dir.iterdir():
        if not proj_dir.is_dir():
            continue

        for jsonl_file in proj_dir.glob("*.jsonl"):
            if jsonl_file.name.startswith("."):
                continue
            st = jsonl_file.stat()
            if st.st_mtime < min_mtime:
                continue

            turns = 0
            related = False
            detected_cwd = None
            first_ts = None
            match_tier = 3

            # Ścieżka projektu może być zakodowana w nazwie katalogu np. -Users-phantom-Documents-AIOS-Vault
            sanitized_target = str(target_resolved).replace("/", "-").replace("\\", "-")
            if sanitized_target in proj_dir.name or target_name in proj_dir.name.lower():
                related = True
                match_tier = 1
                detected_cwd = str(target_resolved)

            try:
                with open(jsonl_file, "r", encoding="utf-8", errors="ignore") as f:
                    for line_idx, line in enumerate(f):
                        if not line.strip():
                            continue
                        turns += 1
                        if line_idx > 50 and related:
                            continue
                        try:
                            item = json.loads(line)
                            if not first_ts and "timestamp" in item:
                                first_ts = item["timestamp"]
                            content_str = str(item)
                            if str(target_resolved) in content_str:
                                related = True
                                match_tier = 1
                                detected_cwd = str(target_resolved)
                        except Exception:
                            pass
            except Exception:
                continue

            if related:
                dt_str = first_ts or datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat()
                sessions.append(
                    SessionMeta(
                        session_id=jsonl_file.stem,
                        harness="claude",
                        file_path=str(jsonl_file),
                        created_at=dt_str,
                        mtime=st.st_mtime,
                        cwd=detected_cwd or str(target_resolved),
                        project_name=target_name,
                        size_bytes=st.st_size,
                        turns_count=turns,
                        match_tier=match_tier,
                    )
                )

    return sorted(sessions, key=lambda s: s.mtime, reverse=True)[:max_count]


def scan_markdown_sessions(
    vault_path: Path,
    min_mtime: float,
    project_filter: Optional[str] = None,
    max_count: int = 100
) -> List[SessionMeta]:
    """Skanuje pliki transkryptów w _brudnopis/ oraz dzienniki w _pamiec/dziennik/."""
    sessions: List[SessionMeta] = []
    
    brudnopis_dir = vault_path / "_brudnopis"
    dziennik_dir = vault_path / "_pamiec" / "dziennik"

    search_targets = [
        (brudnopis_dir, "markdown_brudnopis"),
        (dziennik_dir, "markdown_dziennik"),
    ]

    for s_dir, harness_name in search_targets:
        if not s_dir.exists():
            continue

        for md_file in s_dir.glob("*.md"):
            if md_file.name.startswith((".", "_SZABLON")):
                continue
            st = md_file.stat()
            if st.st_mtime < min_mtime:
                continue

            turns = 1
            project_name = None
            created_at_str = None
            content_sample = ""

            try:
                with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                    content_sample = f.read(4000)
                    
                # Parsowanie prostego frontmatter YAML
                if content_sample.startswith("---"):
                    fm_end = content_sample.find("---", 3)
                    if fm_end != -1:
                        fm_text = content_sample[3:fm_end]
                        for fm_line in fm_text.splitlines():
                            if ":" in fm_line:
                                k, v = fm_line.split(":", 1)
                                k = k.strip().lower()
                                v = v.strip().strip("'\"")
                                if k in ("projekt", "project"):
                                    project_name = v
                                elif k in ("data", "date"):
                                    created_at_str = v

                # Filtrowanie po projekcie jeśli podano
                if project_filter:
                    p_filt = project_filter.lower()
                    if project_name and p_filt not in project_name.lower():
                        if p_filt not in md_file.name.lower() and p_filt not in content_sample.lower():
                            continue

                dt_str = created_at_str or datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat()
                sessions.append(
                    SessionMeta(
                        session_id=md_file.stem,
                        harness=harness_name,
                        file_path=str(md_file),
                        created_at=dt_str,
                        mtime=st.st_mtime,
                        cwd=str(vault_path),
                        project_name=project_name or vault_path.name,
                        size_bytes=st.st_size,
                        turns_count=turns,
                        match_tier=1 if project_name else 2,
                    )
                )
            except Exception:
                continue

    return sorted(sessions, key=lambda s: s.mtime, reverse=True)[:max_count]


def scan_all_sessions(
    target_path: Path,
    since: Optional[str] = "14d",
    harnesses: Optional[List[str]] = None,
    max_sessions: int = 100
) -> List[SessionMeta]:
    """Główna funkcja skanująca sesje z wszystkich źródeł."""
    now_ts = datetime.now(timezone.utc).timestamp()
    duration_sec = parse_duration_to_seconds(since or "14d")
    min_mtime = now_ts - duration_sec

    active_harnesses = [h.lower() for h in harnesses] if harnesses else ["all"]

    all_sessions: List[SessionMeta] = []

    if "all" in active_harnesses or "antigravity" in active_harnesses:
        all_sessions.extend(scan_antigravity_sessions(target_path, min_mtime, max_sessions))

    if "all" in active_harnesses or "claude" in active_harnesses:
        all_sessions.extend(scan_claude_sessions(target_path, min_mtime, max_sessions))

    if "all" in active_harnesses or "markdown" in active_harnesses:
        all_sessions.extend(scan_markdown_sessions(target_path, min_mtime, target_path.name, max_sessions))

    # Sortowanie po dacie modyfikacji malejąco i obcięcie do limitu
    return sorted(all_sessions, key=lambda s: s.mtime, reverse=True)[:max_sessions]


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    res = scan_all_sessions(target, since="14d")
    print(f"Znaleziono {len(res)} sesji dla {target}:")
    for s in res[:10]:
        print(f" - [{s.harness}] {s.session_id} ({s.created_at[:10]}) {s.size_bytes}B {s.turns_count} turns")
