#!/usr/bin/env python3
"""Fetch a YouTube transcript via the Supadata API and print or save it."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen


def extract_video_id(value: str) -> str:
    """Extract a video ID from a raw ID or a YouTube URL."""
    if re.fullmatch(r"[\w-]{11}", value):
        return value

    parsed = urlparse(value)
    host = parsed.netloc.lower()

    if host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.lstrip("/").split("/")[0]
        if re.fullmatch(r"[\w-]{11}", video_id):
            return video_id

    if "youtube.com" in host:
        query_id = parse_qs(parsed.query).get("v", [])
        if query_id and re.fullmatch(r"[\w-]{11}", query_id[0]):
            return query_id[0]

        path_parts = [part for part in parsed.path.split("/") if part]
        if len(path_parts) >= 2 and path_parts[0] in {"embed", "shorts", "live"}:
            candidate = path_parts[1]
            if re.fullmatch(r"[\w-]{11}", candidate):
                return candidate

    raise ValueError(f"Could not extract a YouTube video ID from: {value}")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "youtube-transcript"


def fetch_transcript(
    video_url: str,
    language: str | None,
    plain_text: bool,
    mode: str,
    api_key: str,
    poll_seconds: int,
) -> tuple[list[dict], str]:
    params = {"url": video_url, "mode": mode}
    if language:
        params["lang"] = language
    if plain_text:
        params["text"] = "true"

    query = "https://api.supadata.ai/v1/transcript?" + urlencode(params)
    data = supadata_get_json(query, api_key)

    if "jobId" in data:
        data = wait_for_transcript_job(data["jobId"], api_key, poll_seconds)

    content = data.get("content", "")
    lang = data.get("lang", language or "unknown")

    if isinstance(content, str):
        rows = [{"text": content, "start": 0}]
    else:
        rows = []
        for item in content:
            rows.append(
                {
                    "text": item.get("text", ""),
                    "start": float(item.get("offset", 0)) / 1000,
                    "duration": float(item.get("duration", 0)) / 1000,
                }
            )

    return rows, lang


def supadata_get_json(url: str, api_key: str) -> dict:
    request = Request(
        url,
        headers={
            "x-api-key": api_key,
            "Accept": "application/json",
        },
    )

    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_transcript_job(job_id: str, api_key: str, poll_seconds: int) -> dict:
    job_url = f"https://api.supadata.ai/v1/transcript/{job_id}"
    deadline = time.time() + max(poll_seconds, 1)

    while time.time() < deadline:
        data = supadata_get_json(job_url, api_key)
        status = data.get("status")

        if status == "completed":
            return data
        if status == "failed":
            error = data.get("error", {})
            raise RuntimeError(error.get("message", "Transcript job failed"))

        time.sleep(1)

    raise RuntimeError(
        "Supadata started the transcript job, but it did not finish in time. "
        f"Job ID: {job_id}"
    )


def build_markdown(
    title: str,
    url: str,
    channel: str | None,
    date: str | None,
    language_code: str,
    rows: list[dict],
    include_timestamps: bool,
) -> str:
    lines = [f"# {title}", ""]

    if channel:
        lines.extend([f"**Channel**: {channel}", ""])

    lines.extend([f"**URL**: {url}", ""])

    if date:
        lines.extend([f"**Date**: {date}", ""])

    lines.extend([f"**Language**: {language_code}", "", "## Transcript", ""])

    for row in rows:
        text = " ".join(str(row.get("text", "")).split()).strip()
        if not text:
            continue

        if include_timestamps:
            start = float(row.get("start", 0))
            minutes = int(start // 60)
            seconds = start % 60
            lines.append(f"[{minutes:02d}:{seconds:05.2f}] {text}")
        else:
            lines.append(text)

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube transcript with the Supadata API."
    )
    parser.add_argument("video", help="YouTube URL or 11-character video ID")
    parser.add_argument(
        "--title",
        help="Markdown title to use in the output file",
    )
    parser.add_argument(
        "--channel",
        help="Optional channel or source label",
    )
    parser.add_argument(
        "--date",
        help="Optional publication date to include in the Markdown",
    )
    parser.add_argument(
        "--lang",
        help="Preferred transcript language, for example en.",
    )
    parser.add_argument(
        "--mode",
        choices=["native", "auto", "generate"],
        default="auto",
        help="Supadata transcript mode. Default: auto.",
    )
    parser.add_argument(
        "--api-key",
        help="Supadata API key. If omitted, SUPADATA_API_KEY is used.",
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=90,
        help="How many seconds to wait for longer transcript jobs. Default: 90.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file path. Defaults to stdout.",
    )
    parser.add_argument(
        "--repo-output",
        action="store_true",
        help="Save into research/youtube-transcripts using a slugified title.",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps next to each transcript line.",
    )
    args = parser.parse_args()

    if args.output and args.repo_output:
        parser.error("Use either --output or --repo-output, not both.")

    video_id = extract_video_id(args.video)
    url = f"https://www.youtube.com/watch?v={video_id}"
    title = args.title or f"YouTube Transcript ({video_id})"
    api_key = args.api_key or os.environ.get("SUPADATA_API_KEY")

    if not api_key:
        print(
            "Missing Supadata API key.\n"
            "Set it like this first:\n"
            "export SUPADATA_API_KEY='your_key_here'",
            file=sys.stderr,
        )
        return 1

    try:
        rows, language_code = fetch_transcript(
            video_url=url,
            language=args.lang,
            plain_text=not args.timestamps,
            mode=args.mode,
            api_key=api_key,
            poll_seconds=args.wait,
        )
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"Supadata request failed ({exc.code}): {body}", file=sys.stderr)
        return 1
    except URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - runtime guard
        print(f"Failed to fetch transcript: {exc}", file=sys.stderr)
        return 1

    markdown = build_markdown(
        title=title,
        url=url,
        channel=args.channel,
        date=args.date,
        language_code=language_code,
        rows=rows,
        include_timestamps=args.timestamps,
    )

    output_path: Path | None = args.output
    if args.repo_output:
        output_path = (
            Path("research") / "youtube-transcripts" / f"{slugify(title)}.md"
        )

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"Saved transcript to {output_path}")
    else:
        print(markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
