#!/usr/bin/env python3
"""Render the saved scientific model; centerlines, not an embedding certificate."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;m=json.loads((P/'spatial_model.json').read_text());s=json.loads((P/'surgery_link.json').read_text())
fig=plt.figure(figsize=(12,8));ax=fig.add_subplot(111,projection='3d')
for name,poly in zip(['Base knot R','Unchanged surgery axis a','Original axis b'],m['base_components']):
 p=np.array(poly+[poly[0]]);ax.plot(*p.T,lw=1.1,label=name)
for name,core in zip(['A handle core','B handle core (reverse orientation)'],m['band_cores']):
 p=np.array(core);ax.plot(*p.T,lw=1.8,label=name)
p=np.array(s['splice_core']);ax.plot(*p.T,ls='--',lw=1.6,label='Joining band to b');r=np.array(m['root']);ax.scatter(*r,marker='*',s=100)
ax.text(*(r+[-195,-15,40]),'Marked central disk',fontsize=10)
ax.set_xlabel('x');ax.set_ylabel('y');ax.set_zlabel('z');ax.view_init(elev=24,azim=-65);ax.set_box_aspect((1.25,1,.8));ax.set_title('Explicit marked genus-one correction — spatial model',pad=20);ax.legend(loc='upper left',fontsize=9)
fig.text(.08,.065,r'$A=x_4x_3^{-2}x_1$'+'\n'+r'$B=x_4x_9^{-1}x_1^{-1}x_3x_1^{-1}x_8x_5^{-1}x_8^{-1}x_1^2$',fontsize=12)
fig.text(.08,.015,'Band centerlines are shown for readability. Exact integer-coordinate surfaces, framings and crossings are in the accompanying certificate.',fontsize=9)
fig.subplots_adjust(bottom=.16,top=.9)
for ext in ('png','svg'):fig.savefig(P/('marked_genus_one_spatial.'+ext),dpi=200,bbox_inches='tight')
