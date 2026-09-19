#!/usr/bin/env python3
"""Plot measured bigraded ranks; the highlighted deficits obstruct ribbon arrows."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

d = json.loads(Path('results/nonfibered_khovanov_filter/manifest.json').read_text())
rows = {r['name']: r for r in d['runs']}
degrees = [(-5, -5), (0, -3), (1, -1), (2, 1), (3, 3), (4, 5), (5, 7), (6, 9)]
names = ['K1', 'J24227', 'J25789', 'J25533']
ranks = {name: {(i, j): n for i, j, n in rows[name]['ranks']} for name in names}
fig, ax = plt.subplots(figsize=(11.5, 4.3))
fig.patch.set_facecolor('#fafafa'); ax.set_facecolor('#fafafa')
ax.set_xlim(-0.5, 7.5); ax.set_ylim(3.5, -0.5)
for y, name in enumerate(names):
    for x, degree in enumerate(degrees):
        value = ranks[name].get(degree, 0)
        missing = y > 0 and value < ranks['K1'].get(degree, 0)
        color = '#f9d8d6' if missing else ('#ddeaf4' if y == 0 else '#e5eee6')
        ax.add_patch(plt.Rectangle((x-.47, y-.42), .94, .84, facecolor=color, edgecolor='white'))
        ax.text(x, y, str(value), ha='center', va='center', fontsize=15,
                color='#a52b26' if missing else '#203444', fontweight='bold' if missing else 'normal')
ax.set_xticks(range(8), [f'({i}, {j})' for i, j in degrees], fontsize=11)
ax.set_yticks(range(4), ['K₁ required', 'J24227 — excluded', 'J25789 — excluded', 'J25533 — retained'], fontsize=11)
ax.set_xlabel('Bigrading (homological, quantum)', fontsize=11, labelpad=12)
ax.tick_params(length=0)
for spine in ax.spines.values(): spine.set_visible(False)
fig.suptitle('A large homology group can still be missing the required class', fontsize=15, x=.53, y=.98)
fig.text(.53, .88, 'Unreduced Khovanov ranks over F₂ · red cells violate the ribbon injection inequality', ha='center', fontsize=10)
fig.text(.53, .025, 'J25789 and J25533 differ by one full band twist; both have knot Floer rank 173.\nRetained means this necessary test passes. No K₀–K₁ concordance or slice disk for their difference is known.', ha='center', fontsize=10)
fig.subplots_adjust(left=.23, right=.98, top=.80, bottom=.23)
fig.savefig('figures/khovanov-common-upper-gate.png', dpi=180)
fig.savefig('figures/khovanov-common-upper-gate.pdf')
