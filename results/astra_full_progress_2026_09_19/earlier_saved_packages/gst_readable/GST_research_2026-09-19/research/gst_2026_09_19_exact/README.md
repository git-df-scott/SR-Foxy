# GST48 research package — 19 September 2026

**CE: NO.** Read `REPORT.md` and `STATUS.json` first. Nothing was pushed.

The code/data live together so scripts resolve inputs relative to their own directory. Place this directory under `research/gst_2026_09_19_exact/` in SR-Foxy without changing existing campaign files.

## Replay saved certificates

Tested with Python 3.13.5 on Linux. Install `requirements.txt` in a virtual environment; the repository's existing wheelhouse artifact can alternatively supply the native topology packages.

```sh
python -m pip install -r requirements.txt
python -m knot_floer_homology.test
python verify_algebra.py
python verify_topology.py
python replay_saved.py --level 3 --shards 1 --shard 0
for shard in 0 1 2 3; do
  python replay_saved.py --level 4 --shards 4 --shard "$shard"
done
```

The four shards partition the saved 15,794 band records. Shard zero also replays all 50 saved self-return movies and the 12 separate-variable tail certificates. Sharding avoids a single long tool invocation; no work is scheduled in the background.

## Recreate the searches

```sh
python compute.py
python band_probe.py
python prefix_certify.py
python prime43.py
python verify_algebra.py
python run_hfk_gst.py
python verify_topology.py
python extended_prefix_search.py --max-length 3 --max-twists 1
python multivariable_prefix_certificate.py
python extended_prefix_search.py --max-length 4 --max-twists 2
python analyze_L4_survivors.py
python certify_trivial_L4.py
```

The `analyze_L4_survivors.py` file is an intermediate filter; its `unresolved` entries are subsequently resolved as self-returns by `certify_trivial_L4.py`, then replayed by `replay_saved.py`. No short movie in this package proves GST ribbon: its endpoint is GST plus an unknot, not an unlink.

## Main files

| File | Purpose |
|---|---|
| `gst48.json` | Exact source PD and attribution |
| `STATUS.json` | Final status, environment provenance, counts, and nonclaims |
| `REPORT.md` | Derivations, theorem dependencies, interpretation, and limitations |
| `algebra_certificates.json` | Polynomial factors, Bezout identity, Smith data, and resultants |
| `gst48_uv0_complex.json` | Full 189-generator reduced Floer complex |
| `topology_verification.json` | Independent construction and Floer consistency checks |
| `prefix_certificates.json` | Exact 164 single-face prefix exclusions |
| `multivariable_prefix_certificates.json` | Three exceptional L3/T1 exclusions, full integer matrices |
| `extended_prefix_L4_T2.json` | All 15,794 compressed band specifications and first-stage results |
| `L4_followup.json` | Separate-variable follow-up for 62 first-stage survivors |
| `L4_trivial_movies.json` | All 50 exact self-return movies |
| `replay_L4_shard*_result.json` | Successful partitioned replay results |

Earlier exploratory component/Jones files are retained for auditability. They are not extra live candidates. In particular, sharing an Alexander polynomial with a cable did not identify the component as that cable; the Jones computation differed. The report does not rely on numerical hyperbolic identification or these exploratory classifications.

The archive has a SHA256 manifest. It does not contain the large wheelhouse, credentials, or third-party font files. Source input attribution is in `gst48.json` and the report.
