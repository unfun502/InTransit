"""Eurostat road_go_na_rl3g (national road freight by NUTS-3 region of loading and NST 2007 goods group) ->
public/data/commodity.json: per NUTS-3 code, total kt and share by goods group, plus the dominant family.
Usage: python -I scripts/commodity.py _dl/eurostat/rl3g_2019.csv public/data/commodity.json
"""
import csv, json, sys, collections
src, out = sys.argv[1:3]
GROUPS = {
 'GT01': 'Agricultural products', 'GT02': 'Coal, crude oil, gas', 'GT03': 'Ores, quarrying', 'GT04': 'Food, drink, tobacco',
 'GT05': 'Textiles, leather', 'GT06': 'Wood, paper, print', 'GT07': 'Refined petroleum', 'GT08': 'Chemicals, plastics',
 'GT09': 'Non-metallic minerals', 'GT10': 'Metals', 'GT11': 'Machinery', 'GT12': 'Transport equipment', 'GT13': 'Furniture, other goods',
 'GT14': 'Waste, recycling', 'GT15': 'Mail, parcels', 'GT16': 'Containers, pallets', 'GT17': 'Household removals', 'GT18': 'Grouped goods',
 'GT19': 'Unidentifiable goods', 'GT20': 'Other goods'}
FAMILY = {'GT01': 'agri', 'GT04': 'agri', 'GT02': 'energy', 'GT03': 'energy', 'GT07': 'energy', 'GT09': 'energy',
          'GT10': 'metal', 'GT11': 'metal', 'GT12': 'metal', 'GT08': 'chem', 'GT05': 'consumer', 'GT06': 'consumer', 'GT13': 'consumer',
          'GT14': 'waste', 'GT15': 'mixed', 'GT16': 'mixed', 'GT17': 'mixed', 'GT18': 'mixed', 'GT19': 'mixed', 'GT20': 'mixed'}
FAMILIES = {'agri': 'Agriculture & food', 'energy': 'Energy & minerals', 'metal': 'Metals & machinery', 'chem': 'Chemicals',
            'consumer': 'Consumer & manufactured', 'waste': 'Waste & recycling', 'mixed': 'Mixed & other'}
vals = collections.defaultdict(dict)
for r in csv.DictReader(open(src, encoding='utf-8')):
    g = r['geo']; v = r['OBS_VALUE']
    if len(g) != 5 or v in ('', ':'): continue
    vals[g][r['nst07']] = float(v)
out_d = {}
for g, d in vals.items():
    total = d.get('TOTAL') or sum(v for k, v in d.items() if k != 'TOTAL')
    if not total: continue
    groups = sorted(((k, v) for k, v in d.items() if k != 'TOTAL' and v > 0), key=lambda kv: -kv[1])
    if not groups: continue
    fam = collections.defaultdict(float)
    for k, v in groups: fam[FAMILY[k]] += v
    top_fam = max(fam.items(), key=lambda kv: kv[1])[0]
    out_d[g] = {'t': round(total), 'g': [[k, round(v / total, 3)] for k, v in groups[:6]], 'f': [[k, round(v / total, 3)] for k, v in sorted(fam.items(), key=lambda kv: -kv[1])], 'dom': top_fam}
json.dump({'year': 2019, 'unit': 'thousand tonnes loaded', 'groups': GROUPS, 'families': FAMILIES, 'family_of': FAMILY, 'regions': out_d}, open(out, 'w', encoding='utf-8'), separators=(',', ':'))
import os
dom = collections.Counter(v['dom'] for v in out_d.values())
print('regions', len(out_d), 'bytes', os.path.getsize(out), 'dominant family counts', dict(dom))
