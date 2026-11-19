"""Small enrichments so the page needs less data up front:
- regions.json gains a `nuts` code per region (from regions.geojson), so commodity lookups don't need the polygons.
- meta.json gains the busiest highway segment's corridor profile (from edge_profiles.json), used by the story copy.
Usage: python -I scripts/enrich.py
"""
import json
D = 'public/data/'
regions = json.load(open(D + 'regions.json', encoding='utf-8'))
polys = json.load(open(D + 'regions.geojson', encoding='utf-8'))
nuts = {i: f['properties']['nuts'] for f in polys['features'] for i in f['properties']['ids']}
for r in regions:
    if r['id'] in nuts: r['nuts'] = nuts[r['id']]
json.dump(regions, open(D + 'regions.json', 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
net = json.load(open(D + 'network.json')); ep = json.load(open(D + 'edge_profiles.json')); nodes = json.load(open(D + 'nodes.json'))
e = max(net, key=lambda e: e[4]); p = ep[str(e[0])]
meta = json.load(open(D + 'meta.json'))
meta['busiest'] = {'id': e[0], 'km': e[3], 'trucks19': e[4], 't': p['t'], 'cc': [[c, round(v / p['t'], 3)] for c, v in p['cc']], 'at': nodes[str(e[1])]}
json.dump(meta, open(D + 'meta.json', 'w'), separators=(',', ':'))
print('regions with nuts', sum(1 for r in regions if 'nuts' in r), 'of', len(regions)); print('busiest', meta['busiest'])
