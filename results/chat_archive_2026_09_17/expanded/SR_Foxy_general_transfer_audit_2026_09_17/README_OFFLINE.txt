SR-Foxy pass03 — proposed general transfer theorem, independently unreviewed.
No counterexample. No new files in this package have been pushed.

Read new_results/README.md, then new_results/PROPOSED_TRANSFER_THEOREM.md.
Algebra reproduction (Python standard library only):
  python3 new_results/check_general_transfer.py --output FRESH_RESULTS.json
Direct new ribbon controls (requires SymPy, g++, Boost):
  python3 new_results/check_connected_sum_controls.py dependencies/pass02 FRESH_CONTROL_DIR --maximum 3

The additions-only patch targets only a new directory under results/astra_2026_09_17_overnight/.
Inspect git status and run git apply --check before applying. It refuses existing paths.
Do not create a branch, reset, overwrite work, or assume an unreviewed proof closes a research route.
The unchanged pass02 dependency files are bundled only to enable offline reproduction.
