"""Independent exact determinant check of a sliceness obstruction for the control."""
import json,sys
from pathlib import Path
import snappy,sympy
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from colored_link_rank import fox_matrix,rank_minor
r=json.loads((p/'SQUARE_PAIR_NONRIBBON_CONTROL.json').read_text());L=snappy.Link(r['pd']);mat,colors=fox_matrix(L,[2,2],101);a=rank_minor(mat,len(colors),101)
minor=[[mat[i][j] for j in a['minor_columns']] for i in a['minor_rows']];independent=int(sympy.Matrix(minor).det())%101
assert a['maximal_minor_nonzero'] and independent==a['minor_determinant_mod_prime']==83
out={**a,'prime':101,'component_values':[2,2],'generator_components':colors,'fox_matrix_mod_prime':mat,'independent_sympy_minor_determinant_mod_prime':independent,'conclusion':'Nonzero maximal Alexander minor obstructs strong sliceness. This nonribbon control is not a Slice-Ribbon counterexample.'}
(p/'SQUARE_PAIR_ALEXANDER_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(out['conclusion'])
