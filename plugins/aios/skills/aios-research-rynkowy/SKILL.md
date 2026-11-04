---
name: aios-research-rynkowy
description: Use when the user wants to do secondary research - find out how other companies solved a similar problem, or whether there is academic / industry evidence supporting a working hypothesis. Triggers on "desk research", "research wtórny", "literature review", "scholar review", "competitive analysis", "co inni zrobili z [problem]", "czy są na to badania", "evidence-based decision", "literature scan", "industry benchmark research", /research-rynkowy, /aios-research-rynkowy, /aios:research-rynkowy. Dispatches two parallel sub-agents - competitive scan + scholar scan - both forced to surface disconfirming evidence. Output is a report saved to the project's research/ folder. Does NOT touch ost-state.json.
---

# Desk Research

Guided workflow: frame the question with the user, design queries together, dispatch two parallel sub-agents (competitive + scholar), synthesize, produce a report with mandatory disconfirming evidence. Mirror the user's language and vocabulary from their project files throughout.

## Reference load map

Load each file only at the stage indicated:

| Stage | Load |
|-------|------|
| 0 (Setup) | `assets/state-template.json` |
| 3 (Dispatch) | `assets/shared-subagent-base.md` + `assets/competitive-subagent-prompt.md` or `assets/scholar-subagent-prompt.md` |
| 4 (Synthesis) | `references/quality-rubric.md` (re-check confidence) |
| 5 (Report) | `references/report-template.md` |

## Hard rules (always active)

1. **Confront the hypothesis, don't confirm it.** At least 1/3 of the report must address disconfirming evidence.
2. **Every finding needs a URL.** No URL = not a finding.
3. **Minimum 3 independent sources for High confidence.** Three articles citing the same McKinsey report = 1 source.
4. **Vendor sources flagged, not hidden.** Confidence capped at Low. Tagged `[VENDOR]` in bibliography.
5. **Never modify `ost-state.json`.**

## Lazy user mode

If user signals disengagement (`"skip"`, `""`, `"."`', or equivalent in their language): auto-decide, say what you picked and why in one sentence, mark `auto_decided: true` in state, continue. **Exception:** disconfirmation prompt (Stage 1.4) - if skipped, note `disconfirmation_skipped: true` and inform sub-agents to strengthen their falsification mandate.

## Workflow

```
Setup → Brief gate → Query design gate → Sub-agent dispatch (||) → Synthesis gate → Report
```

If invoked on existing state, jump to the stage matching `current_stage` (see Resume routing at end).

---

## Stage 0 - Setup

### 0.1 Detect existing state

Look for `desk-research-state-*.json` in the project folder or `<project>/research/`. If found, offer via `AskUserQuestion`: resume / jump to stage / start new (archive old).

### 0.2 Ingest project context

Scan active project folder (`Projekty/<kategoria>/<nazwa>/`):
- `brief.md`, `*-brief.md` - problem framing
- `research/*.md` - read first 80 lines of EVERY .md file (carry the working thesis)
- `analyses/*.md` - read first 80 lines of EVERY .md file
- `ost-state.json` - if present, read `brief.outcome.statement` + top 2-3 opportunities by PRES total (read-only)
- Note `*.csv`/`*.xlsx` filenames in `analyses/` (don't load contents)

Extract `industry_or_domain` from brief.md. If project folder empty, ask directly.

### 0.3 Confirm scope

`AskUserQuestion`, single-choice:
- Single problem (default)
- Broader literature scan (sets scale=deep)
- Competitive only (disables sub-agent B)
- Scholar only (disables sub-agent A)

Initialize `desk-research-state.json` from `assets/state-template.json`.

---

## Stage 1 - Research brief gate

### 1.1 Extract from context

From ingested files, formulate:
- **Problem statement** - one falsifiable sentence
- **Working hypothesis** - what user already assumes (often unstated - extract from brief/OST/newest research file)
- **Decision at stake** - what gets approved/rejected based on this research

If you can't extract any of the three, ask directly. Don't invent.

### 1.2 Propose 3-5 research questions

Each must be falsifiable. Frame as testable questions ("Does X correlate with Y?", "How strongly does...", "Under what conditions...", "How much..."). Not essay topics.

Show numbered list, then `AskUserQuestion` single-choice: OK / cut question N / rephrase N / add new. Loop until user says OK.

### 1.3 Adaptive scale

Based on approved question count:
- 1-3 questions → quick: ~5-7 sources/sub-agent, report 1-2 pages
- 4-5 questions → deep: ~15+ sources/sub-agent, full report

Tell user the scale explicitly. `AskUserQuestion` with override option.

### 1.4 Disconfirmation prompt (soft gate)

Open prompt: ask what evidence would prove the hypothesis WRONG. Accept any answer. If skipped, mark `disconfirmation_skipped: true`.

### 1.5 Show full brief & confirm

Display the full brief (problem, hypothesis, decision at stake, questions, scale, falsification criterion). Gate: OK / edit / stop and discuss.

---

## Stage 2 - Query design gate

### 2.1 Competitive queries

For each research question generate:
- **Companies/cases** - 5-10 names (mix leaders + niche + adjacent industry)
- **Keywords** - 3-5 English phrases for WebSearch
- **Recency** - default 5 years
- **Source heuristics** - prioritize trade press, analyst reports, case studies; flag vendor whitepapers

### 2.2 Scholar queries

Map user's business language to academic language explicitly. Show the mapping table to the user - this is where they often add a key term.

Format: `USER LANGUAGE → ACADEMIC LANGUAGE` with 1-2 query strings per mapping for `site:scholar.google.com` via WebSearch.

### 2.3 Show & confirm queries

`AskUserQuestion` with all queries listed. Options to edit/add/remove. Save final queries to state.

---

## Stage 3 - Sub-agent dispatch (parallel)

Dispatch both sub-agents in ONE message as two parallel `Agent` tool calls.

### 3.1 Sub-agent A - Competitive scan

Read `assets/shared-subagent-base.md` and `assets/competitive-subagent-prompt.md`. The competitive prompt extends the shared base. Substitute all `{{placeholders}}` from state:

| Placeholder | Source |
|---|---|
| `{{problem_statement}}` | `state.brief.problem_statement` |
| `{{working_hypothesis}}` | `state.brief.working_hypothesis` |
| `{{decision_at_stake}}` | `state.brief.decision_at_stake` |
| `{{numbered_research_questions}}` | numbered list from `state.brief.research_questions` |
| `{{disconfirmation_criterion_OR_skipped_message}}` | criterion verbatim, or if skipped: "User skipped the falsification criterion. Your mandate for the disconfirming section is stronger: minimum 4 disconfirming findings at confidence Medium+." |
| `{{companies_to_investigate}}` | from state |
| `{{search_keywords}}` | from state |
| `{{source_heuristics}}` | from state |
| `{{industry_or_domain}}` | from state |
| `{{project_path}}` | from state |
| `{{recency_window_years}}` | from state |
| `{{recency_start_year}}` | computed |
| `{{current_year}}` | computed |
| `{{quick_OR_deep}}` | `state.brief.scale` |

Output: structured findings file at `{project_path}/research/.desk-tmp/competitive-findings-<ts>.md` + 200-word summary.

### 3.2 Sub-agent B - Scholar scan

Read `assets/shared-subagent-base.md` and `assets/scholar-subagent-prompt.md`. Additional placeholders: `{{scholar_term_mappings}}`, `{{scholar_search_queries}}`.

Output: findings file at `{project_path}/research/.desk-tmp/scholar-findings-<ts>.md` + 200-word summary.

### 3.3 Failure handling

- Competitive empty → queries too narrow, loop back to 2.1
- Scholar empty → may be genuinely under-researched (legitimate finding), flag in Gaps
- Both empty → ask user: bad queries / under-researched / network issue? Single-choice + open-ended

---

## Stage 4 - Synthesis gate

### 4.1 Read both findings files

Open full files from sub-agents.

### 4.2 Cluster per research question

For each question, gather evidence from both streams. Working format per question: competitive findings (N, confidence, source), scholar findings (N, confidence, source), confrontation with hypothesis (supports/refutes/mixed), strongest quotes/numbers.

### 4.3 Cross-source contradictions

Find points where competitive and scholar disagree. These are the most valuable synthesis fragments. Patterns: case study says "worked" but scholar says "only under condition Y"; multiple firms adopted solution X but scholar shows small effect size; seminal paper supports it but industry moved away.

### 4.4 Disconfirming evidence

Dedicate a section to everything contradicting the user's hypothesis. If <3 points at confidence Medium+, send sub-agents back for more.

### 4.5 Show synthesis & confirm

Show user: strongest conclusion + strongest counter-evidence. Gate: write report / go back for more counter-evidence / go back for more on topic X / stop and discuss.

---

## Stage 5 - Report

### 5.1 Generate

Read `references/report-template.md`. Follow it exactly.

### 5.2 Save & link

File: `<project>/research/<YYYY-MM-DD>-desk-<short-topic>.md`. Update state to `complete`. Clean up `.desk-tmp/` (delete by default unless user wants full logs).

### 5.3 Wrap-up

Short message: report link, one-line TL;DR, strongest counter-evidence to watch, next steps suggestion.

---

## Red flags - STOP

- Report has no/empty disconfirming section → back to 4.4
- Bibliography >50% vendor sources → back to 2.1
- Recommending "supported" with <3 independent High-confidence sources → note limitation in TL;DR
- Sub-agent returns citations without URL → reject, make them fix it
- Disconfirmation skipped AND disconfirming section <3 points → escalate to user
- Recency: >50% competitive sources >5 years → flag drift

---

## Iteration mode

When user returns to an existing report wanting more:
1. Load state + existing report
2. Identify which stage to repeat (typically 3 with new queries or 2 with better mappings)
3. Dispatch sub-agents with differential queries only
4. Append `## Iteracja [data]` to report (before bibliography)
5. If disposition changes: preserve original TL;DR as blockquote, write new TL;DR, update frontmatter

---

## Resume routing

| `current_stage` | Action |
|---|---|
| `setup` | Start from 0.1 |
| `brief` | Show existing brief for approval/edit |
| `queries` | Show existing queries for approval |
| `dispatch` | Check sub-agent statuses: both complete → go to 4; one complete → re-dispatch missing; both pending/failed → re-dispatch both; both in_progress → ask user: re-run or recover from `.desk-tmp/`? |
| `synthesis` | Stage 4 with existing findings + draft |
| `report` | Stage 5.1 (synthesis approved, just needs file) |
| `complete` | Offer iteration mode |

---

## Conversational style

- Always show citations with suggestions. One question at a time, max 4 options + open-ended.
- Push back on thin evidence. If user accepts a conclusion with <2 sources, surface it.
- Be honest about gaps. Mirror user's vocabulary from their project files.

## File conventions

- State: `<project>/research/desk-research-state.json`
- Temp findings: `<project>/research/.desk-tmp/`
- Final report: `<project>/research/<YYYY-MM-DD>-desk-<short-topic>.md`
- Never write to `4-Knowledge/`
