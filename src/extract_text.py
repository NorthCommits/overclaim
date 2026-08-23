"""
Stage 2a: convert letter PDFs to plain text.

Mechanical only, no parsing. Extraction logic gets re-run many times
and re-reading PDFs each round is wasted time.
"""

from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
LETTER_DIR = ROOT / "data" / "raw" / "letters"
TEXT_DIR = ROOT / "data" / "interim" / "letters_text"

MIN_CHARS = 500


def main():
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(LETTER_DIR.glob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs")

    ok = short = failed = 0

    for pdf in pdfs:
        target = TEXT_DIR / f"{pdf.stem}.txt"
        try:
            with pymupdf.open(pdf) as doc:
                pages = [page.get_text() for page in doc]
            text = "\n".join(pages)
        except Exception as exc:
            failed += 1
            print(f"  failed {pdf.stem}: {exc}")
            continue

        target.write_text(text, encoding="utf-8")

        if len(text) < MIN_CHARS:
            short += 1
            print(f"  short {pdf.stem}: {len(text)} chars, {len(pages)} pages")
        else:
            ok += 1

    print(f"\nok={ok} short={short} failed={failed}")


if __name__ == "__main__":
    main()