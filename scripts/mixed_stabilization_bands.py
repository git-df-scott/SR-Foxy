"""Biased face-simple bands interacting with all three connected-sum factors.

Endpoint factors are K0 and mirror(K1); an interior crossing side belongs to
J. Twist is solved to make the resulting two-component linking number zero.
Every emitted band is replayable. This is sampling, never exhaustive coverage.
"""
from spherogram.links.bands.core import Band, add_one_band, normalize_crossing_labels
from nonfibered_reverse_audit import sampled_bands


def generate(parent, parameters, job, counts):
    groups = job.get('factor_crossing_counts')
    if groups:
        assert len(groups) == 3 and sum(groups) == len(parent.crossings)
        a, b = groups[0], groups[0] + groups[1]
        def group(index):
            return 0 if index < a else 1 if index < b else 2
    assert len(parent.link_components) == 1
    normalize_crossing_labels(parent)
    seen = set()
    for band, metadata in sampled_bands(parent, parameters['seed'],
                                       parameters.get('attempts', 100000),
                                       max_length=parameters['length'], max_twists=1):
        counts['sampled_paths'] += 1
        if groups:
            ends = {group(band.cs_along_top[i][0]) for i in (0, -1)}
            interior = {group(c) for c, side in band.cs_along_top[1:-1]}
            if ends != {0, 1} or 2 not in interior:
                counts['not_three_factor_interaction'] += 1
                continue
        base = add_one_band(parent, band)
        assert len(base.link_components) == 2 and base.is_planar()
        linking = int(base.linking_number())
        solutions = []
        for twists in sorted({band.num_twist-2*abs(linking), band.num_twist+2*abs(linking)}):
            adjusted = Band(band.cs_along_top, band.arc_is_under, twists)
            result = add_one_band(parent, adjusted)
            if result.linking_number() == 0:
                solutions.append((adjusted, result))
        assert len(solutions) == 1
        adjusted, result = solutions[0]
        if abs(adjusted.num_twist) > parameters['twists']:
            counts['twist_limit_skipped'] += 1
            continue
        spec = adjusted.compressed_spec()
        if spec in seen:
            continue
        seen.add(spec)
        normalize_crossing_labels(result)
        yield result, spec
