"""Spatial-join Fraunhofer region centroids to NUTS-3 polygons (GISCO GeoJSON) and write public/data/regions.geojson.
Usage: python -I scripts/polygons.py _dl/nuts/nuts3_2016_10M.geojson public/data/regions.json public/data/regions.geojson
"""
import json, sys, collections
nuts_path, regions_path, out_path = sys.argv[1:4]
nuts = json.load(open(nuts_path, encoding='utf-8'))
regions = json.load(open(regions_path, encoding='utf-8'))

def rings(geom):
    if geom['type'] == 'Polygon': yield geom['coordinates']
    elif geom['type'] == 'MultiPolygon':
        for p in geom['coordinates']: yield p
def bbox(geom):
    xs, ys = [], []
    for poly in rings(geom):
        for x, y in poly[0]: xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)
def inside(pt, ring):
    x, y = pt; n = len(ring); j = n - 1; ok = False
    for i in range(n):
        xi, yi = ring[i]; xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-300) + xi: ok = not ok
        j = i
    return ok
def contains(geom, pt):
    for poly in rings(geom):
        if inside(pt, poly[0]) and not any(inside(pt, hole) for hole in poly[1:]): return True
    return False

feats = [(f, bbox(f['geometry'])) for f in nuts['features']]
matched, unmatched = [], collections.Counter(); by_nuts = {}
used = collections.Counter()
for r in regions:
    pt = (r['lng'], r['lat']); hit = None
    for f, (x0, y0, x1, y1) in feats:
        if x0 <= pt[0] <= x1 and y0 <= pt[1] <= y1 and contains(f['geometry'], pt): hit = f; break
    if hit:
        nid = hit['properties']['NUTS_ID']; used[nid] += 1
        if nid in by_nuts: by_nuts[nid]['properties']['ids'].append(r['id'])   # ETISplus zone finer than NUTS 2016: share the polygon
        else:
            by_nuts[nid] = {'type': 'Feature', 'geometry': hit['geometry'], 'properties': {'nuts': nid, 'ids': [r['id']], 'cc': r['cc']}}
            matched.append(by_nuts[nid])
    else: unmatched[r['cc']] += 1

# round coordinates to 4 decimals (~10 m) to keep the file small
def rnd(c): return [rnd(x) for x in c] if isinstance(c[0], list) else [round(c[0], 4), round(c[1], 4)]
for f in matched: f['geometry']['coordinates'] = rnd(f['geometry']['coordinates'])
json.dump({'type': 'FeatureCollection', 'features': matched}, open(out_path, 'w', encoding='utf-8'), separators=(',', ':'))
print('regions', len(regions), 'matched', len(matched), 'unmatched by country', dict(unmatched))
print('polygons shared by >1 region:', sum(1 for v in used.values() if v > 1))
import os; print('output bytes', os.path.getsize(out_path))
