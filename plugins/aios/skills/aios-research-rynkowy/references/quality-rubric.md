# Quality Rubric

Applied by sub-agents when scoring findings, and re-checked at synthesis (Stage 4).

## Confidence Levels

| Confidence | Criteria |
|------------|----------|
| **High** | 3+ independent sources agree; at least one non-vendor; recent (≤5yr competitive, ≤10yr scholar); has effect size or concrete numbers |
| **Medium** | 2 independent sources, OR 1 strong one (peer-reviewed, well-documented case study with numbers); no red flags |
| **Low** | Single source; echo-chamber sources; >5yr without confirmation; vendor-only; no numbers |

Below Low (hearsay, social media, vendor blog with no data) = doesn't enter the report. Exception: if it illustrates a popular claim the evidence doesn't support, it lives in the disconfirming section.

## Independence

Three articles citing the same underlying report = one source, not three. Check:
- **Author independence** - different research groups
- **Funding independence** - different sponsors
- **Citation independence** - not just citing each other in a cluster

For any High-confidence finding, you must be able to point to 3 distinct clusters.

## Vendor Sources

Vendor = company with commercial interest in the claim being true. Rules:
- Flagged `[VENDOR]` in bibliography, not excluded
- Confidence capped at Low regardless of how many vendors agree
- If >50% sources in a section are vendor: warn in the report
- Vendor case study with externally verifiable numbers → upgrade to Medium

Industry-funded academic paper (disclosed) → flag `industry_funded`, cap = Medium.

## Recency

Competitive default 5 years, scholar 10 years. Seminal papers (100+ citations) have no time limit but must be cited alongside a recent application. Older findings without recent corroboration → cap Medium with flag.

Fast-moving domains (consumer behavior, mobile, social): be stricter. Slow-moving (B2B, regulated): can relax to 7-10yr.

## Effect Sizes

Prefer numbers over qualitative claims. Hierarchy: meta-analysis > RCT/A/B test with effect size > quasi-experimental (before/after) > observational (flag: correlation not causation) > case study without numbers (cap Low) > anecdote (not a finding).

If no effect size available, mark: "qualitative finding, no effect size reported."

## Edge Cases

- **Seminal paper (>10yr, 100+ citations):** Confidence Medium (single source), unless recent replications exist. Always cite alongside a recent paper.
- **Disconfirming evidence at Low confidence:** Still include it - the disconfirming section intentionally has a lower bar than confirming. Flag the asymmetry.
- **Conflicting results in one source** (e.g., +15% conversion but +8% returns): Report as one compound finding. Don't cherry-pick.
