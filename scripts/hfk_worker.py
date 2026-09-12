#!/usr/bin/env python3
"""One isolated HFK calculation; callers impose a hard process timeout."""
import json
import sys
import knot_floer_homology

if __name__=='__main__':
    # The direct PD API avoids importing the full topology stack per case.
    h=knot_floer_homology.pd_to_hfk(json.load(sys.stdin))
    print(json.dumps({'ranks':[[a,m,n] for (a,m),n in sorted(h['ranks'].items())],
                      'total_rank':h['total_rank'],'fibered':h['fibered'],
                      'seifert_genus':h['seifert_genus'],'tau':h['tau']}))
