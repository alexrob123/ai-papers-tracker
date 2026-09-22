# ai-papers-tracker

Tracks new AI research papers from a set of sources and emails you when a
new one shows up. Currently supports:

- [Anthropic Research](https://www.anthropic.com/research)

Known papers are stored in [`data/papers.json`](data/papers.json), keyed by
URL. A GitHub Actions workflow runs on a schedule, diffs the current source
listing against that file, emails any new entries, and commits the updated
file back to the repo.

## Latest papers
*Auto-updated by the scheduled workflow — do not edit this table by hand.*

<!-- LATEST_PAPERS:START -->
| Date | Source | Category | Title |
| --- | --- | --- | --- |
| 2026-09-17 | Anthropic | Science | [How Claude is uplifting biomolecular modeling](https://www.anthropic.com/research/claude-uplifts-biomolecular-modeling) |
| 2026-09-10 | Anthropic | Frontier Red Team | [Measuring tactical intelligence targeting and conventional weapons capabilities of AI models](https://www.anthropic.com/research/intelligence-targeting-conventional-weapons-capabilities) |
| 2026-09-09 | Anthropic | Alignment | [An alignment assessment of recent cybersecurity incidents](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) |
| 2026-09-04 | Anthropic | Science | [Formalizing Fermat's Last Theorem](https://www.anthropic.com/research/formalizing-fermats-last-theorem) |
| 2026-08-28 | Anthropic | Alignment | [Automated researchers can reliably mitigate alignment failures](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures) |
| 2026-08-26 | Anthropic | Societal Impacts | [Enabling independent research on how people use Claude](https://www.anthropic.com/research/enabling-independent-research) |
| 2026-08-18 | Anthropic | Science | [How Claude is accelerating protein design and analytical chemistry](https://www.anthropic.com/research/Claude-accelerates-protein-design) |
| 2026-08-13 | Anthropic | Frontier Red Team | [Patterns and problems in emerging multiagent systems](https://www.anthropic.com/research/multiagent-systems) |
| 2026-08-12 | Anthropic | Economics | [Reviewing the evidence on worker retraining programs](https://www.anthropic.com/research/reviewing-the-evidence-on-worker-retraining-programs) |
| 2026-08-10 | Anthropic | Science | [Learning more about Claude's mathematical capabilities](https://www.anthropic.com/research/riemann-zeta) |
<!-- LATEST_PAPERS:END -->



## How it works

- `tracker/sources/` — one module per source. Each exposes a `NAME` and a
  `fetch() -> list[Paper]` function.
- `tracker/storage.py` — loads/saves the known-papers JSON file.
- `tracker/notifier.py` — sends an email (via SMTP) listing the new papers.
- `main.py` — CLI entrypoint that ties it together.

## Running locally

```bash
uv sync
uv run main.py check --dry-run   # see what's new, without emailing or saving
uv run main.py check --no-notify # save new papers to data/papers.json without emailing
uv run main.py check             # normal run: email new papers and save them
```

Email sending requires these environment variables (see below):
`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `MAIL_TO`, `MAIL_FROM`
(optional, defaults to `SMTP_USER`).

## Setting up email notifications (Gmail)

1. Enable 2-Step Verification on the Gmail account you want to send from.
2. Create an [App Password](https://myaccount.google.com/apppasswords) for
   it (choose "Mail" / "Other").
3. In the GitHub repo, go to **Settings → Secrets and variables → Actions**
   and add:
   - `SMTP_HOST` = `smtp.gmail.com`
   - `SMTP_PORT` = `587`
   - `SMTP_USER` = your Gmail address
   - `SMTP_PASS` = the 16-character app password
   - `MAIL_TO` = the address that should receive notifications

## Scheduling

[`.github/workflows/check-papers.yml`](.github/workflows/check-papers.yml)
runs daily (13:00 UTC) and can also be triggered manually from the Actions
tab (`workflow_dispatch`). It checks all sources, emails anything new, and
commits the updated `data/papers.json` and the "Latest papers" table above
back to `main`.

## Adding a new source

1. Create `tracker/sources/<name>.py` with a `NAME` constant and a
   `fetch() -> list[Paper]` function that returns one `Paper` per item
   (`source`, `title`, `url`, `date` as an ISO date string, and an optional
   `category`).
2. Register it in `tracker/sources/__init__.py`'s `SOURCES` dict.

No other changes are needed — storage, diffing, and notification are
source-agnostic.
