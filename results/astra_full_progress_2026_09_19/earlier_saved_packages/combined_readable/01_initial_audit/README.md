# SR-Foxy night-session preparation

**Counterexample found: no.** This package is an audit and an executable night-session handoff, not a new knot certificate.

Read `TONIGHT_HANDOFF.md` for the new Opus session. `AUDIT.md` explains the newly identified inference defects. `audit_regressions.py` executes 16 bounded tests, including synthetic comparison counterexamples and a reproduction of the existing SL(2,F5) axis obstruction. `results.json` and `run.log` preserve their outputs. `coverage.json` records what was and was not read. `sources.json` records primary references, theorem locations, and verification limits.

Run with Python 3.10 or newer:

```sh
python3 audit_regressions.py
```

To save a rerun, choose an unused destination with `--output`. No third-party packages are required. Output creation is exclusive so previous evidence cannot be overwritten accidentally.

These files were created in a separate Linux working directory. Nothing was pushed to GitHub, no branch was created, and the Mac checkout was not changed. No remote census data or active job status was recovered. No computation continues after this package was produced.
