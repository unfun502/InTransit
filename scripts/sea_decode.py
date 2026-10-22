"""Decode the Eurostat JSON-stat maritime files (mar_go_am_<cc>, 2019, by port, partner, direction, cargo) into _dl/sea/rows.json
and print the partner codes and the ports without UN/LOCODE coordinates, for building the anchor table."""
import json, csv, glob, re, collections, os
coords = {}
for r in csv.DictReader(open('_dl/sea/unlocode.csv', encoding='utf-8')):
    m = re.match(r'(\d{2})(\d{2})([NS]) (\d{3})(\d{2})([EW])', r['Coordinates'] or '')
    if m:
        lat = (int(m[1]) + int(m[2]) / 60) * (1 if m[3] == 'N' else -1); lon = (int(m[4]) + int(m[5]) / 60) * (1 if m[6] == 'E' else -1)
        coords[r['Country'] + r['Location']] = [round(lon, 3), round(lat, 3)]
rows = []; ports = {}; partners = {}; cargos = {}
for f in sorted(glob.glob('_dl/sea/cargo/*.json')):
    d = json.load(open(f, encoding='utf-8'))
    if 'value' not in d: print('skip', f, d.get('error', '')[:80]); continue
    dims, size = d['id'], d['size']; cats = {k: d['dimension'][k]['category'] for k in dims}
    strides = []; s = 1
    for n in reversed(size): strides.insert(0, s); s *= n
    inv = {k: {i: code for code, i in cats[k]['index'].items()} for k in dims}
    cargos.update(cats['cargo']['label'])
    for key, v in d['value'].items():
        key = int(key); sel = {k: inv[k][key // strides[i] % size[i]] for i, k in enumerate(dims)}
        rep, par, direct, cargo = sel['rep_mar'], sel['par_mar'], sel['direct'], sel['cargo']
        m = re.match(r'^([A-Z]{2})_\d([A-Z]{5})$', rep)   # port codes: country, sea-area digit, UN/LOCODE (e.g. NL_0NLRTM, UK_1GBABD)
        if not m or direct == 'TOTAL' or v <= 0: continue
        loc = m[2]
        ports.setdefault(rep, {'id': rep, 'loc': loc, 'name': cats['rep_mar']['label'][rep], 'cc': rep[:2], 'xy': coords.get(loc)})
        partners[par] = cats['par_mar']['label'][par]
        rows.append([rep, par, direct, cargo, v])
json.dump({'rows': rows, 'ports': ports, 'partners': partners, 'cargos': cargos}, open('_dl/sea/rows.json', 'w', encoding='utf-8'))
print('rows', len(rows), 'ports', len(ports), 'located', sum(1 for p in ports.values() if p['xy']), 'partners', len(partners))
print('cargo codes:', cargos)
tot = collections.Counter()
for rep, par, direct, cargo, v in rows:
    if cargo == 'TOTAL': tot[par] += v
print('--- partners by tonnage (code, label, kt):')
for par, v in tot.most_common(): print(f'{par:14} {v:>10,.0f}  {partners[par]}')
print('--- unlocated ports:')
for p in ports.values():
    if not p['xy']: print(p['id'], p['name'])
