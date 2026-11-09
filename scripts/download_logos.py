#!/usr/bin/env python3
"""Download the EnableArt logo and favicon from https://enableart.ai.

Usage:
    python scripts/download_logos.py              # saves into <project>/assets/
    python scripts/download_logos.py --out DIR    # saves into DIR

Only the Python standard library is used.
"""
import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://www.enableart.ai"
FILES = ["images/logo.png", "images/favicon.png"]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PROJECT_DIR = Path(__file__).resolve().parent.parent


def download(rel_path: str, out_dir: Path) -> Path:
    url = f"{BASE_URL}/{rel_path}"
    req = urllib.request.Request(url, headers={"User-Agent": "enableart-asset-downloader/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(f"{url} did not return a PNG image")
    dest = out_dir / Path(rel_path).name
    dest.write_bytes(data)
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=PROJECT_DIR / "assets",
                        help="output directory (default: <project>/assets)")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    failed = 0
    for rel in FILES:
        try:
            dest = download(rel, args.out)
            print(f"OK    {rel} -> {dest} ({dest.stat().st_size} bytes)")
        except (urllib.error.URLError, ValueError, OSError) as exc:
            failed += 1
            print(f"FAIL  {rel}: {exc}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
