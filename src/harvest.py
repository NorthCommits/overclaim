"""
Stage 1: harvest OPDP untitled letters.

Fetches the FDA index page, parses it into a manifest, and downloads
letter PDFs. Idempotent: re-running skips PDFs already on disk.

Promotional material URLs are recorded in the manifest but never
fetched. Those documents are company copyright.
"""
from pathlib import Path
from urllib.parse import urljoin

import httpx
import csv
import re
import time
from datetime import date, datetime
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

INDEX_URL = (
    "https://www.fda.gov/drugs/"
    "warning-letters-and-notice-violation-letters-pharmaceutical-companies/"
    "untitled-letters"
)
USER_AGENT = "overclaim-dataset/0.1 (research; contact via github.com/NorthCommits/overclaim)"
MIN_EXPECTED_ROWS = 50
REQUEST_DELAY = 1.0

ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT / "data" / "raw" / "index"
LETTER_DIR = ROOT / "data" / "raw" / "letters"
MANIFEST = ROOT / "data" / "interim" / "letters_manifest.csv"

MEDIA_ID = re.compile(r"/media/(\d+)/download")


def fetch_index(client):
    resp = client.get(INDEX_URL)
    resp.raise_for_status()
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    (INDEX_DIR / f"index_{stamp}.html").write_text(resp.text, encoding="utf-8")
    return resp.text


def parse_date(raw):
    raw = raw.strip()
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return ""


def media_id(url):
    match = MEDIA_ID.search(url)
    return match.group(1) if match else ""


def parse_rows(html):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if table is None:
        raise RuntimeError("No table found on index page")

    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all("td")
        if len(cells) < 3:
            continue

        letter_url = ""
        promo_urls = []
        for a in cells[1].find_all("a", href=True):
            label = a.get_text(strip=True).lower()
            href = a["href"]
            if "untitled letter" in label and not letter_url:
                letter_url = urljoin(INDEX_URL, href)
            elif "promotional material" in label:
                promo_urls.append(urljoin(INDEX_URL, href))

        close_out = ""
        if len(cells) >= 5:
            link = cells[4].find("a", href=True)
            if link:
                close_out = urljoin(INDEX_URL, link["href"])

        rows.append(
            {
                "media_id": media_id(letter_url),
                "letter_date": parse_date(cells[0].get_text()),
                "company": cells[1].get_text(" ", strip=True).split("Untitled Letter")[0].strip(),
                "product_raw": cells[2].get_text(" ", strip=True),
                "letter_url": letter_url,
                "promo_material_urls": "|".join(promo_urls),
                "close_out_url": close_out,
                "retrieved_at": date.today().isoformat(),
            }
        )
    return rows


def write_manifest(rows):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def download_letters(client, rows):
    LETTER_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = skipped = failed = 0

    for row in rows:
        mid = row["media_id"]
        if not mid:
            failed += 1
            print(f"  no media id: {row['letter_date']} {row['product_raw'][:40]}")
            continue

        target = LETTER_DIR / f"{mid}.pdf"
        if target.exists():
            skipped += 1
            continue

        try:
            resp = client.get(row["letter_url"])
            resp.raise_for_status()
            target.write_bytes(resp.content)
            downloaded += 1
            print(f"  got {mid}.pdf ({len(resp.content)} bytes)")
        except Exception as exc:
            failed += 1
            print(f"  failed {mid}: {exc}")

        time.sleep(REQUEST_DELAY)

    return downloaded, skipped, failed


def main():
    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(headers=headers, timeout=60.0, follow_redirects=True) as client:
        print("Fetching index")
        html = fetch_index(client)

        rows = parse_rows(html)
        print(f"Parsed {len(rows)} rows")
        if len(rows) < MIN_EXPECTED_ROWS:
            raise RuntimeError(
                f"Only {len(rows)} rows parsed, expected at least {MIN_EXPECTED_ROWS}. "
                "The page structure may have changed."
            )

        write_manifest(rows)
        print(f"Wrote {MANIFEST}")

        print("Downloading letters")
        downloaded, skipped, failed = download_letters(client, rows)
        print(f"\ndownloaded={downloaded} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()