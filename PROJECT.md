# Carpenter - project brief

Venice.ai reads this file with every request. Describe here what Carpenter is and the decisions that should
hold across changes; Venice will keep it up to date as the code grows.

## What Carpenter is

_(Write a few sentences: what the app does, who uses it, and on what - Windows PC, Linux PC or Android phone.)_

## Decisions

- A BeeWare app: screens with **Toga** in `carpenter/app.py`, packaged with **Briefcase** (`pyproject.toml`)
  for **Windows, Linux and Android**. Python 3.12.
- Logic lives in plain modules in `carpenter/` that do not import toga (e.g. `carpenter/core.py`), so it can
  be tested; `app.py` only builds the screens.
- Tests in `tests/` (pytest), never importing toga.
- Run-time packages go in `pyproject.toml` (`requires`) and `requirements.txt`; they must work on Android.
- Secrets (API keys, passwords) come from environment variables, never from code.

## Done so far

- Project skeleton, the Venice → GitHub pipeline, and the Windows / Linux / Android builds.
- A first screen: type a name, press *Say hello*.
