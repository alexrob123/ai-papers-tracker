from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

from .models import Paper


def _required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def send_new_paper_email(papers: list[Paper]) -> None:
    if not papers:
        return

    host = _required_env("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT") or "587")
    user = _required_env("SMTP_USER")
    password = _required_env("SMTP_PASS")
    mail_to = _required_env("MAIL_TO")
    mail_from = os.environ.get("MAIL_FROM") or user

    subject = f"{len(papers)} new AI research paper{'s' if len(papers) != 1 else ''} found"

    lines = []
    for paper in sorted(papers, key=lambda p: p.date, reverse=True):
        category = f" [{paper.category}]" if paper.category else ""
        lines.append(f"- {paper.date} ({paper.source}){category}: {paper.title}\n  {paper.url}")

    body = "New papers detected:\n\n" + "\n\n".join(lines) + "\n"

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = mail_from
    message["To"] = mail_to
    message.set_content(body)

    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(user, password)
        smtp.send_message(message)
