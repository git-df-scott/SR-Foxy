"""Construct an exact word-level conjugacy repair invisible to the boundary
Alexander module. This does NOT construct an embedded axis or annulus.
"""
from pathlib import Path
import contextlib
import io
import json

p=Path(__file__).with_name('collar_module.py')
ns={'__file__':str(p)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(p.read_text(),str(p),'exec'),ns)

def inverse(w):
    return [-v for v in w[::-1]]

def reduce_word(w):
    out=[]
    for x in w:
        if out and out[-1]==-x:
            out.pop()
        else:
            out.append(x)
    return out

# The source images use only generators 5,6,8. These have literal upper-factor
# lifts: boundary generators 3,4,8 respectively, using one-based conventions.
lift_generator={5:3,6:4,8:8}
assert all(ns['images'][v]==[k] for k,v in lift_generator.items())
lift=lambda w:[(1 if x>0 else -1)*lift_generator[abs(x)] for x in w]
w1,w2=ns['repair_words']
mu=ns['images'][5]
image1,image2=ns['push'](w1),ns['push'](w2)
target=reduce_word(inverse(mu)+image1+mu)
delta_source=reduce_word(target+inverse(image2))
delta=lift(delta_source)
assert ns['push'](delta)==delta_source
coords=ns['ns']['coords']
assert coords(delta)==[0,0]
assert ns['source_class'](delta_source)==0
assert sum(1 if x>0 else -1 for x in delta)==0
new_w2=reduce_word(delta+w2)
assert reduce_word(ns['push'](new_w2))==target
assert coords(new_w2)==coords(w2)
# Exact conjugacy is proved by free reduction, stronger than trace equality.
identity=reduce_word(inverse(target)+ns['push'](new_w2))
assert identity==[]
assert delta_source!=[]
# Test whether this particular based word is merely a replacement of the
# lower connector U L V -> U w L w^-1 V. A nonzero trace difference forbids it
# already after applying q0. This is not a test of all freely conjugate axes.
p=Path(__file__).with_name('winding_trace.py')
rep={'__file__':str(p)}
exec(compile(p.read_text().split('traces=[];words=[]')[0],str(p),'exec'),rep)
U,L,V=[4,-1],[-15,14,-13,17],[3,-4]
assert U+L+V==w2
inner=reduce_word(inverse(U)+new_w2+inverse(V))
trace_diff=rep['red'](rep['s'].trace(rep['val'](inner,rep['col']))-rep['s'].trace(rep['val'](L,rep['col'])))
print(json.dumps({'status':'WORD_LEVEL_ONLY_NOT_A_GEOMETRIC_BAND_OR_ANNULUS','source_upper_lifts':lift_generator,'original_axis1':w1,'original_axis2':w2,'seam_meridian_boundary_generator':5,'correction_source_word':delta_source,'correction_boundary_word':delta,'corrected_axis2':new_w2,'correction_boundary_F_coordinates':[str(v) for v in coords(delta)],'lengths':{'source_correction':len(delta_source),'corrected_boundary_axis2':len(new_w2)},'checks':{'q0_corrected_axis2_equals_mu_inverse_q0_axis1_mu_by_free_reduction':True,'correction_boundary_module_zero':True,'axis2_boundary_module_unchanged':True,'geometric_axis_unlink_or_response_certified':False},'identity_residue':identity,'fixed_based_connector_test':{'old_prefix':U,'old_lower_segment':L,'old_suffix':V,'required_inner_trace_minus_old_trace':str(trace_diff),'excluded_as_pure_lower_conjugation_of_this_based_word':trace_diff!=0}},indent=2))
