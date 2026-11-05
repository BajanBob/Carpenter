# Carpenter

Carpenter is built by **Venice.ai** from plain-language requests. Each request becomes a pull request that
is checked automatically and merged only when you approve it.

```
 you: "Add a command that ..."      (Actions → Venice code intake → Run workflow)
   ▼
 tools/venice_bridge.py ── Venice API (api.venice.ai, OpenAI-compatible, function calling)
   │  Venice gets your request, PROJECT.md and the file list, reads the files it needs,
   │  and hands in its change. The change is tried on a scratch copy first; if an edit
   │  does not match or the Python does not compile, Venice is told and fixes it (3 tries).
   ▼
 .github/workflows/venice-intake.yml
   1. checks every path (nothing in .git/, .github/ or tools/, nothing outside the repo)
   2. writes the change to a branch venice/<name>  (never main)
   3. checks: requirements install, every Python file compiles, `pytest` passes
   4. opens a pull request (a draft marked FAILED if a check fails)
   ▼
 you review → Merge
```

## Making a request

1. Open **Actions → Venice code intake → Run workflow** (works on a phone).
2. Type the request in **Task**, for example
   *"Create a command-line tool in carpenter/cli.py that lists the files in a folder with their sizes,
   with tests."*
3. Tick **Test only** to try it without opening a pull request, or leave it unticked.
4. Press **Run workflow**. After a few minutes the pull request appears under **Pull requests**: read it,
   then **Merge** if you are happy, or close it.

To change an open pull request, run another request that names the same branch, e.g.
*"On branch venice/file-lister: also show the total size."*

Tips for good results:
- One feature per request; say what it should do, not how.
- Ask for tests - the checks only prove what the tests cover.
- Keep **PROJECT.md** up to date: Venice reads it with every request, so it decides what Carpenter is.

## Settings (already done)

- Secret `VENICE_API_KEY` (Settings → Secrets and variables → Actions): your Venice inference key.
- Workflow permissions: read and write, and Actions may create pull requests.
- Optional variable `VENICE_MODEL` (same page, Variables tab) to choose the Venice model. Default:
  `qwen3-coder-480b-a35b-instruct-turbo`. Other Venice coding models with function calling:
  `kimi-k2-7-code`, `openai-gpt-53-codex`.

Venice API use is billed to your Venice account; keep a monthly spend limit on the key.

## From a computer (optional)

```
set VENICE_API_KEY=...                       (Windows;  export ... on Linux / Mac)
python tools/venice_bridge.py "your request" --dry-run    see what Venice writes, send nothing
set GITHUB_TOKEN=github_pat_...              (fine-grained token: only this repo, Contents read/write)
python tools/venice_bridge.py "your request" --send       open the pull request
python tools/venice_send.py --title "..." file1.py file2.py   send files you saved yourself
```

## Layout

| path | what |
|---|---|
| `carpenter/` | the application (Python package) |
| `tests/` | tests (pytest) - run by the checks on every change |
| `PROJECT.md` | the brief: what Carpenter is, decisions made - Venice reads it every time |
| `requirements.txt` | Python packages Carpenter needs |
| `tools/`, `.github/` | the pipeline - changed only by a person |
