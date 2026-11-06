# Carpenter - project brief

Its your builder of that I idea stuck in your head

## What Carpenter is

_(You maybe at the beach or at a bus stop and you can use your phone to instruct Carpenter to supervise Venice.ai and github to execute that project in less than 5 minutes  )_

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
- Added Jsonn encrypted bidirectional chat with white noise modulation.
