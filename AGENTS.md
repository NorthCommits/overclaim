# overclaim

## What this is
A dataset of pharmaceutical promotional claims labelled as substantiated or
overstated, built from FDA enforcement letters and matched against approved
product labels. Labels come from regulators, not annotators.

## Non-negotiable constraints
- Public domain US government sources only: FDA letter archives, openFDA,
  DailyMed. Nothing else enters the dataset.
- Never include client, employer, or otherwise proprietary material.
- Promotional pieces referenced by letters are company copyright. Store only
  the excerpts FDA quotes inside the letter body. Never fetch or store the
  source advertisement itself.
- Data is never committed to git. Code and notes only.

## Provenance
Every row carries the source letter URL, the letter issue date, the retrieval
date, and the openFDA identifier of the matched label. A row missing any of
these is a bug, not an edge case.

## Pipeline
Four stages. Each reads from disk and writes to disk, so any stage can be
re-run without re-running the one before it.
1. harvest: fetch the letter index and letter documents
2. extract: letters to structured claim records
3. match: claims to supporting or contradicting label text
4. package: validate, assemble, write parquet

Intermediate output lives in data/raw, data/interim, data/processed.
All of data/ is gitignored.

## Working agreements
- Do not write pipeline code until the schema is agreed in notes/schema.md.
- Propose the approach before implementing. One file at a time.
- Keep the structure simple. No abstraction until the same pattern has
  appeared three times.
- No emojis and no em dashes in code, comments, docs, or commit messages.
- After each change, run it and show the raw output rather than describing it.

## Environment
Python 3.12, uv for packaging, ruff for linting, pytest for tests.

## Current state
Recon phase. No pipeline code exists. Findings go in notes/letter-recon.md.