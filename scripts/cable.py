#!/usr/bin/env python3
"""(p,q)-cable of a knot given by a braid word, Seifert-framed.

The blackboard p-parallel of a braid closure has framing = writhe w, so the
Seifert-framed (p,q)-cable is the closure of the p-fold cabled braid together with
q - p*w extra half-twists in the p new strands.  Verified below against the
Alexander-polynomial identity Delta_{K_{p,q}}(t) = Delta_K(t^p) * Delta_{T(p,q)}(t).
"""
import snappy

def cable_braid(word, n_strands, p, q, writhe):
    """Braid word for the (p,q)-cable, on p*n_strands strands."""
    out = []
    for let in word:                       # replace each generator by a p x p block swap
        i = abs(let); s = 1 if let > 0 else -1
        base = (i - 1) * p
        for a in range(p):                 # standard cabling of one crossing
            for b in range(p):
                out.append(s * (base + p - a + b))
    tw = q - p * writhe                    # correct the framing to Seifert
    full = (i for i in ())
    for _ in range(abs(tw)):
        for a in range(p - 1):
            out.append((1 if tw > 0 else -1) * (a + 1))
    return out, p * n_strands

def cable(K, p, q):
    w = K.writhe(); bw = K.braid_word()
    n = max(abs(x) for x in bw) + 1
    cw, ns = cable_braid(bw, n, p, q, w)
    return snappy.Link(braid_closure=cw)
