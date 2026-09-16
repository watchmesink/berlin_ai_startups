#!/usr/bin/env python3
"""Validate directory and jobs-tracker Markdown for this repo."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
JOBS = ROOT / "AI_PM_ROLES_IN_GERMANY.md"

ENTRY_RE = re.compile(r"\*\*\[([^\]]+)\]\((https?://[^)]+)\)\*\*:")
JOB_CO_RE = re.compile(r"^## \[([^\]]+)\]\((https?://[^)]+)\)", re.M)
ROLE_RE = re.compile(r"^- \[", re.M)
TOC_RE = re.compile(r"\[[^\]]+\]\(#[^)]+\) · (\d+)")
FENCE_RE = re.compile(r"```.*?```", re.S)
MD_LINK_RE = re.compile(r"\[(?:[^\]]+)\]\((https?://[^)]+)\)")


def fail(errors: list[str]) -> int:
    if not errors:
        print("check.py: ok")
        return 0
    print(f"check.py: {len(errors)} error(s)")
    for err in errors:
        print(f"  - {err}")
    return 1


def strip_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def readme_companies(text: str) -> list[tuple[str, str]]:
    return [
        (name, url)
        for name, url in ENTRY_RE.findall(strip_fences(text))
        if url != "https://site"
    ]


def dangling_urls(text: str) -> list[str]:
    bad: list[str] = []
    for url in MD_LINK_RE.findall(text):
        if url.endswith("%") or re.search(r"%[0-9A-Fa-f]$", url):
            bad.append(url)
        if url.endswith("%28") or url.endswith("%28all-g"):
            bad.append(url)
        if re.search(r"-(?:Eng|all-g)$", url):
            bad.append(url)
    return bad


def collect_readme_meta(text: str) -> dict[str, tuple[str, str]]:
    found: dict[str, tuple[str, str]] = {}
    for match in re.finditer(
        r"\*\*\[([^\]]+)\]\((https?://[^)]+)\)\*\*:.*?\n(  👥[^\n]+)",
        strip_fences(text),
        re.S,
    ):
        found[match.group(1).casefold()] = (
            match.group(2),
            match.group(3).replace("<br>", "").rstrip(),
        )
    return found


def collect_jobs_meta(text: str) -> dict[str, tuple[str, str]]:
    found: dict[str, tuple[str, str]] = {}
    for match in re.finditer(
        r"^## \[([^\]]+)\]\((https?://[^)]+)\)\n\n.*?\n(  👥[^\n]+)",
        text,
        re.M | re.S,
    ):
        found[match.group(1).casefold()] = (
            match.group(2),
            match.group(3).replace("<br>", "").rstrip(),
        )
    return found


def main() -> int:
    errors: list[str] = []
    readme = README.read_text(encoding="utf-8")
    jobs = JOBS.read_text(encoding="utf-8")

    companies = readme_companies(readme)
    names = [name for name, _ in companies]
    urls = [url for _, url in companies]

    headline = re.search(r"directory of (\d+) active", readme)
    if not headline:
        errors.append("README headline company count missing")
    elif int(headline.group(1)) != len(companies):
        errors.append(
            f"README headline count {headline.group(1)} != entries {len(companies)}"
        )

    toc_nums = [int(n) for n in TOC_RE.findall(readme)]
    if sum(toc_nums) != len(companies):
        errors.append(f"TOC sum {sum(toc_nums)} != entries {len(companies)}")

    dup_names = sorted({name for name in names if names.count(name) > 1})
    if dup_names:
        errors.append(f"duplicate README names: {dup_names}")
    dup_urls = sorted({url for url in urls if urls.count(url) > 1})
    if dup_urls:
        errors.append(f"duplicate README urls: {dup_urls}")

    job_cos = JOB_CO_RE.findall(jobs)
    roles = ROLE_RE.findall(jobs)
    jobs_intro = re.search(r"\*\*(\d+) roles across (\d+) companies\*\*", jobs)
    if not jobs_intro:
        errors.append("jobs intro role/company counts missing")
    else:
        if int(jobs_intro.group(1)) != len(roles):
            errors.append(
                f"jobs intro roles {jobs_intro.group(1)} != bullets {len(roles)}"
            )
        if int(jobs_intro.group(2)) != len(job_cos):
            errors.append(
                f"jobs intro companies {jobs_intro.group(2)} != headings {len(job_cos)}"
            )

    table = re.search(
        r"The single jobs tracker: (\d+) roles across (\d+) companies", readme
    )
    if not table:
        errors.append("README jobs table counts missing")
    else:
        if int(table.group(1)) != len(roles):
            errors.append(
                f"README table roles {table.group(1)} != jobs bullets {len(roles)}"
            )
        if int(table.group(2)) != len(job_cos):
            errors.append(
                f"README table companies {table.group(2)} != jobs headings {len(job_cos)}"
            )

    job_names = [name for name, _ in job_cos]
    if len(job_names) != len({name.casefold() for name in job_names}):
        errors.append("duplicate jobs-tracker company headings")

    for url in dangling_urls(readme) + dangling_urls(jobs):
        errors.append(f"truncated or dangling URL: {url}")

    readme_meta = collect_readme_meta(readme)
    jobs_meta = collect_jobs_meta(jobs)
    overlap = set(readme_meta) & set(jobs_meta)
    for key in sorted(overlap):
        readme_url, readme_line = readme_meta[key]
        jobs_url, jobs_line = jobs_meta[key]
        if readme_url != jobs_url:
            errors.append(f"URL mismatch for {key}: README {readme_url} vs jobs {jobs_url}")
        if readme_line != jobs_line:
            errors.append(f"metadata mismatch for {key}")

    if len(overlap) < 30:
        errors.append(f"expected ~32 overlapping companies, found {len(overlap)}")

    return fail(errors)


if __name__ == "__main__":
    sys.exit(main())
