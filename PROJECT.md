# Carpenter - project brief

Venice.ai reads this file with every request. Describe here what Carpenter is and the decisions that should
hold across changes; Venice will keep it up to date as the code grows.

## What Carpenter is

_(Write a few sentences: what the app does, who uses it, on what - desktop, web, phone, Raspberry Pi.)_

## Decisions

- Language: Python 3.10 or newer.
- Application code lives in the `carpenter/` package; tests in `tests/` (pytest).
- Prefer the Python standard library; new packages go in `requirements.txt` with a minimum version.
- Secrets (API keys, passwords) come from environment variables, never from code.

## Done so far

- Project skeleton and the Venice → GitHub pipeline.
