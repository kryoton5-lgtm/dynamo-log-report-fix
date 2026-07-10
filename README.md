# log-report — repaired Terminal-Bench task

A Harbor/Terminal-Bench task: parse the Apache-style access log at `/app/access.log` and write a JSON summary report to `/app/report.json` with exactly three keys — `total_requests` (non-empty request lines), `unique_ips` (distinct client IPs, first field per line), and `top_path` (most-requested path from the quoted HTTP request field).

This repo is the repaired version of an intentionally broken task bundle. The fixes:

1. Removed `environment/solution_hint.py` (a leaked copy of the reference solution) from the agent image.
2. Pinned the base image to the allowlisted `python:3.13-slim-bookworm` by `@sha256` digest instead of `python:latest`.
3. `tests/test.sh` now writes the reward to `/logs/verifier/reward.txt` (it wrote to `/app/reward.txt`, where the harness never looks), emits `/logs/verifier/ctrf.json`, and always exits 0.
4. Replaced the existence-only verifier with one test per numbered success criterion: exact JSON schema (exactly the three keys), exact JSON types (`int` that is not `bool`, `str`), exact values computed from the fixed log (6 / 3 / `/index.html`), plus a SHA-256 integrity check that fails if `/app/access.log` was modified.
5. `task.toml` now declares the real artifact (`["/app/report.json"]` — the original named a file nothing writes) and carries substantive difficulty/solution/verification explanations.
6. Rewrote `instruction.md` with absolute paths, the exact output schema, five numbered criteria mirroring the tests 1:1, and the required closing timeout line matching `[agent].timeout_sec`.
7. Hardened `solution/solve.py` to fail loudly on malformed request lines instead of silently skipping them.

## Environment

Single image (`environment/Dockerfile`), reused for the agent and verifier runs: digest-pinned `python:3.13-slim-bookworm` plus pinned `pytest==8.4.1` and `pytest-json-ctrf==0.3.5`. The agent sees only `/app/access.log`; `solution/` and `tests/` are never copied into the image.

## Verification

Validated locally with Harbor 0.18.0 (run from this directory):

```
harbor run -p . -a oracle     # reward 1.0 — run twice, identical
harbor run -p . --agent nop   # reward 0.0 — run twice, identical
```

Image cleanliness: `docker run --rm <image> /bin/bash -lc 'find / \( -name solve.sh -o -name test.sh \) 2>/dev/null'` prints nothing, and `/app` contains only `access.log`.
