#!/usr/bin/env python3
import json
from pathlib import Path
if not __debug__:raise RuntimeError("Assertions must be enabled")

import sympy as s,math
rows=json.loads(Path(__file__).with_name("SCAN.json").read_text())
row=rows[6];assert row["bits"]==[False,True,True,False]
z,n=s.symbols("z n");R=z**6+3*z**5+5*z**4+4*z**3+2*z**2+z+1
P=sum(v*z**j*n**i for i,a in enumerate(row["trace_difference"]) for j,v in enumerate(a))
D=s.rem(s.discriminant(P,n),R,z)
assert D==-336*z**5-1652*z**4-1816*z**3-804*z**2-268*z-572
norm=int(s.resultant(R,D,z));k=math.isqrt(norm)
assert norm==199282855936 and k*k<norm<(k+1)**2
print(json.dumps({"status":"GENERAL_CENTRALIZER_OBSTRUCTION_VERIFIED","norm":norm,"sqrt_floor":k}))
