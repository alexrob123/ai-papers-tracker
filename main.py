from __future__ import annotations

import argparse
from pathlib import Path

from tracker.models import Paper
from tracker.notifier import send_new_paper_email
from tracker.readme import render_table, update_readme
from tracker.sources import SOURCES
from tracker.storage import load_known_papers, save_known_papers

DATA_PATH = Path(__file__).parent / "data" / "papers.json"
README_PATH = Path(__file__).parent / "README.md"


def check(*, notify: bool, dry_run: bool) -> None:
    known = load_known_papers(DATA_PATH)
    new_papers: list[Paper] = []

    for name, fetch in SOURCES.items():
        print(f"Checking source: {name}")
        try:
            fetched = fetch()
        except Exception as exc:
            print(f"  failed to fetch {name}: {exc}")
            continue

        for paper in fetched:
            if paper.url not in known:
                print(f"  new: {paper.title}")
                new_papers.append(paper)
                known[paper.url] = paper.to_dict()

    if new_papers:
        print(f"Found {len(new_papers)} new paper(s).")
        if notify and not dry_run:
            send_new_paper_email(new_papers)
            print("Notification email sent.")
    else:
        print("No new papers found.")

    if not dry_run:
        save_known_papers(DATA_PATH, known)
        print(f"Updated {DATA_PATH}")

        table = render_table(list(known.values()))
        if update_readme(README_PATH, table):
            print(f"Updated {README_PATH}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Track new AI research papers and email on new finds."
    )
    parser.add_argument(
        "command", nargs="?", default="check", choices=["check"], help="Command to run"
    )
    parser.add_argument(
        "--no-notify",
        action="store_true",
        help="Update storage without sending email (e.g. first-run bootstrap)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not send email or write storage; just print what would happen",
    )
    args = parser.parse_args()

    check(notify=not args.no_notify, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
