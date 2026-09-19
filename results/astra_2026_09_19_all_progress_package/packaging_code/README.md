# Packaging and recovery helpers

`VERIFY_PACKAGE.py` at the delivery root is the portable, read-only integrity
checker. `requirements-topology.txt` is a convenience copy of the versions
recorded by the research; it is not represented as an earlier committed file.

Other scripts in this directory are the actual recovery/assembly helpers used
in the isolated `/mnt/data` runtime. They retain their original runtime paths
and are preserved as a record, not a one-command installer or a complete archive
fetcher. They do not contain credentials. Do not run them against a live checkout.
The source export workflow is the exact read-only workflow committed to existing
main for this delivery. Its execution completed before this package was issued.
No helper automatically resumes the mathematical search or pushes changes.
