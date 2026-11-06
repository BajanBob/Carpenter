# Changelog

## 1.1.0 (2026-11-05)

- Add `carpenter/chat.py`: a Jsonn chat module (toy repeating-key XOR obfuscation, not real encryption), with tests.
- `jsonn_decrypt` now raises a clean `ValueError` on a wrong key or corrupted data instead of crashing.

## 1.0.0 (2026-11-05)

- First version: project skeleton, the Venice.ai -> GitHub pipeline, and Windows / Linux / Android builds.
