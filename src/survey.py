"""
Stage 2b: survey the text corpus before writing extraction logic.

Counts how often the structural markers found during recon actually
appear across all 115 letters. Read-only, writes nothing.
"""

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "data" / "interim" / "letters_text"

PATTERNS = {
    "re_block": re.compile(r"^RE:\s", re.MULTILINE),
    "app_number": re.compile(r"\b(?:NDA|BLA|ANDA)\s+\d{6}\b"),
    "misleading_impression": re.compile(r"misleading impression", re.IGNORECASE),
    "when_this_is_not": re.compile(r"when this (?:is|has) not", re.IGNORECASE),
    "we_acknowledge": re.compile(r"[Ww]e acknowledge"),
    "however": re.compile(r"\bHowever,"),
    "requested_action": re.compile(r"Conclusion and Requested Action", re.IGNORECASE),
    "pi_section": re.compile(r"\b(?:INDICATIONS AND USAGE|CLINICAL STUDIES|"
                             r"WARNINGS AND PRECAUTIONS|DOSAGE AND ADMINISTRATION|"
                             r"ADVERSE REACTIONS|CONTRAINDICATIONS)\b"),
    "post_hoc": re.compile(r"post.hoc", re.IGNORECASE),
    "open_label": re.compile(r"open.label", re.IGNORECASE),
    "superiority": re.compile(r"superiorit", re.IGNORECASE),
    "risk_minimiz": re.compile(r"minimiz\w* the risk", re.IGNORECASE),
    "timestamp": re.compile(r"\(\d{1,2}:\d{2}\)"),
}

QUOTE = re.compile(r"[\u201c]([^\u201d]{15,600})[\u201d]")


def main():
    files = sorted(TEXT_DIR.glob("*.txt"))
    print(f"Surveying {len(files)} letters\n")

    hits = Counter()
    quote_counts = []
    lengths = []

    for path in files:
        text = path.read_text(encoding="utf-8")
        lengths.append(len(text))
        quote_counts.append(len(QUOTE.findall(text)))
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                hits[name] += 1

    total = len(files)
    print("Marker presence:")
    for name in PATTERNS:
        n = hits[name]
        print(f"  {name:24s} {n:4d} / {total}  ({100 * n / total:.0f}%)")

    quote_counts.sort()
    lengths.sort()
    print(f"\nCurly quotes per letter:")
    print(f"  min={quote_counts[0]} median={quote_counts[total // 2]} max={quote_counts[-1]}")
    print(f"  total quoted spans across corpus: {sum(quote_counts)}")
    print(f"\nChars per letter:")
    print(f"  min={lengths[0]} median={lengths[total // 2]} max={lengths[-1]}")


if __name__ == "__main__":
    main()