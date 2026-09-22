# ai-papers-tracker

Tracks new AI research papers from a set of sources and emails you when a
new one shows up. Currently supports:

- [Anthropic Research](https://www.anthropic.com/research)
- [OpenAI Research](https://openai.com/research/index/) — the page itself is
  behind a Cloudflare JS challenge, so this reads it from OpenAI's public
  [news RSS feed](https://openai.com/news/rss.xml) instead, filtered to the
  "Research", "Publication", and "Security" categories.

Each source only tracks a specific set of topic categories, listed as a
constant near the top of its file (`INCLUDED_CATEGORIES` in
[`tracker/sources/anthropic.py`](tracker/sources/anthropic.py),
`TRACKED_CATEGORIES` in
[`tracker/sources/openai.py`](tracker/sources/openai.py)) — add or remove
an entry there to change what gets tracked.

Known papers are stored in [`data/papers.json`](data/papers.json), keyed by
URL. A GitHub Actions workflow runs on a schedule, diffs the current source
listing against that file, emails any new entries, and commits the updated
file back to the repo.

## Latest papers
*Auto-updated by the scheduled workflow — do not edit this table by hand.*

<!-- LATEST_PAPERS:START -->
| Date | Source | Type | Category | Title |
| --- | --- | --- | --- | --- |
| 2026‑09‑17 | Anthropic | Post | Science | [How Claude is uplifting biomolecular modeling](https://www.anthropic.com/research/claude-uplifts-biomolecular-modeling) |
| 2026‑09‑16 | OpenAI | Post | Research | [Our framework for reporting model misalignment](https://openai.com/index/model-misalignment-reporting-framework) |
| 2026‑09‑10 | Anthropic | Post | Frontier Red Team | [Measuring tactical intelligence targeting and conventional weapons capabilities of AI models](https://www.anthropic.com/research/intelligence-targeting-conventional-weapons-capabilities) |
| 2026‑09‑09 | Anthropic | Post | Alignment | [An alignment assessment of recent cybersecurity incidents](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) |
| 2026‑09‑08 | OpenAI | Post | Research | [On the Navier–Stokes Millennium Prize Problem](https://openai.com/index/navier-stokes-solution) |
| 2026‑09‑06 | OpenAI | Post | Research | [Research acceleration: The view inside OpenAI](https://openai.com/index/research-acceleration-view-inside-openai) |
| 2026‑09‑04 | Anthropic | Post | Science | [Formalizing Fermat's Last Theorem](https://www.anthropic.com/research/formalizing-fermats-last-theorem) |
| 2026‑09‑03 | OpenAI | Post | Security | [Daybreak for Frontline Defenders: $1B to protect essential services](https://openai.com/index/daybreak-for-frontline-defenders) |
| 2026‑09‑03 | OpenAI | Post | Research | [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra) |
| 2026‑08‑28 | Anthropic | Post | Alignment | [Automated researchers can reliably mitigate alignment failures](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures) |
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
runs daily at 8am Europe/Paris time (a small gate job picks the right UTC
cron trigger across the CET/CEST switch) and can also be triggered manually
from the Actions tab (`workflow_dispatch`). It checks all sources, emails
anything new, and commits the updated `data/papers.json` and the "Latest
papers" table above back to `main`.

## Adding a new source

1. Create `tracker/sources/<name>.py` with a `NAME` constant and a
   `fetch() -> list[Paper]` function that returns one `Paper` per item
   (`source`, `title`, `url`, `date` as an ISO date string, `type` — e.g.
   "Post", "Paper", "Technical report", "Software", "Article" — and an
   optional `category`).
2. Register it in `tracker/sources/__init__.py`'s `SOURCES` dict.

No other changes are needed — storage, diffing, and notification are
source-agnostic.
