"""Build public/data/sea.json from the decoded Eurostat maritime rows (_dl/sea/rows.json):
ports with coordinates and totals, partner anchors, and sea lanes (port -> partner area) routed over sea lanes with searoute.
Usage: python scripts/sea_build.py   (not -I: it imports searoute from site-packages)
"""
import json, csv, re, time, os, sys, urllib.request, urllib.parse, collections
sys.path.insert(0, os.path.dirname(__file__))
from sea_anchors import ANCHORS, SKIP
import searoute as sr

D = json.load(open('_dl/sea/rows.json', encoding='utf-8'))
rows, ports, partners, cargos = D['rows'], D['ports'], D['partners'], D['cargos']

# ---- port coordinates: UN/LOCODE by code, then by name in the same country, then Nominatim (cached) ----
byname = collections.defaultdict(list)
for r in csv.DictReader(open('_dl/sea/unlocode.csv', encoding='utf-8')):
    m = re.match(r'(\d{2})(\d{2})([NS]) (\d{3})(\d{2})([EW])', r['Coordinates'] or '')
    if m:
        lat = (int(m[1]) + int(m[2]) / 60) * (1 if m[3] == 'N' else -1); lon = (int(m[4]) + int(m[5]) / 60) * (1 if m[6] == 'E' else -1)
        byname[(r['Country'], r['NameWoDiacritics'].lower())].append([round(lon, 3), round(lat, 3)])
CACHE = '_dl/sea/geocode_cache.json'
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
CC_ISO = {'EL': 'GR', 'UK': 'GB'}
def geocode(name, cc):
    key = f'{cc}|{name}'
    if key in cache: return cache[key]
    q = re.sub(r'\(.*?\)', '', name).split(',')[0].split(' - ')[0].strip()
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({'q': q, 'countrycodes': CC_ISO.get(cc, cc).lower(), 'format': 'json', 'limit': 1})
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'InTransit demo (devlab502@proton.me)'})
        res = json.load(urllib.request.urlopen(req, timeout=20))
        cache[key] = [round(float(res[0]['lon']), 3), round(float(res[0]['lat']), 3)] if res else None
    except Exception as ex:
        print('geocode failed', name, ex); cache[key] = None
    time.sleep(1.1)
    json.dump(cache, open(CACHE, 'w'))
    return cache[key]
for p in ports.values():
    if p['xy']: continue
    nm = re.sub(r'\(.*?\)', '', p['name']).strip().lower()
    hit = byname.get((CC_ISO.get(p['cc'], p['cc']), nm)) or byname.get((p['cc'], nm))
    p['xy'] = hit[0] if hit else geocode(p['name'], p['cc'])
located = {k: p for k, p in ports.items() if p['xy']}
print('ports', len(ports), 'located', len(located), 'dropped:', [p['name'] for p in ports.values() if not p['xy']][:10])

# ---- aggregate: port totals, and lanes keyed (port, partner, direction) with a cargo breakdown ----
totals = {k: {'in': 0, 'out': 0, 'cargo': collections.Counter()} for k in located}
lanes = collections.defaultdict(lambda: {'kt': 0, 'cargo': collections.Counter()})
for rep, par, direct, cargo, v in rows:
    if rep not in located: continue
    d = 'in' if direct == 'IN' else 'out'
    if par == 'TOTAL':
        if cargo == 'TOTAL': totals[rep][d] += v
        else: totals[rep]['cargo'][cargo] += v
        continue
    if par in SKIP: continue
    L = lanes[(rep, par, d)]
    if cargo == 'TOTAL': L['kt'] += v
    else: L['cargo'][cargo] += v
# prefer the most specific partner level: drop a country row when the same port+direction has rows for that country's sub-areas
keys = list(lanes)
subs = collections.defaultdict(set)
for rep, par, d in keys:
    if '_' in par and par.split('_')[0] not in ('CN', 'UNK', 'AGG'): subs[(rep, d)].add(par.split('_')[0])
for k in keys:
    rep, par, d = k
    if '_' not in par and par in subs[(rep, d)]: del lanes[k]
# resolve anchors
def anchor_of(par):
    if par in ANCHORS: return par
    base = par.split('_')[0]
    return base if base in ANCHORS else None
resolved = []
for (rep, par, d), L in lanes.items():
    a = anchor_of(par)
    if not a or L['kt'] <= 0: continue
    resolved.append({'p': rep, 'par': par, 'a': a, 'dir': d, 'kt': round(L['kt']), 'cargo': {c: round(v) for c, v in L['cargo'].most_common(4)}})
resolved.sort(key=lambda x: -x['kt'])
# keep: top 1,200 overall plus each port's top 5 per direction
keep = set(id(x) for x in resolved[:1200])
perport = collections.defaultdict(list)
for x in resolved: perport[(x['p'], x['dir'])].append(x)
for lst in perport.values():
    for x in lst[:5]: keep.add(id(x))
sel = [x for x in resolved if id(x) in keep]
print('lanes resolved', len(resolved), 'kept', len(sel))

# ---- route each unique (port, anchor) pair over sea lanes ----
routes = {}; failed = 0; t0 = time.time()
pairs = sorted({(x['p'], x['a']) for x in sel})
for i, (rep, a) in enumerate(pairs):
    src = located[rep]['xy']; dst = ANCHORS[a][:2]
    try:
        r = sr.searoute(src, list(dst), units='km')
        pts = r['geometry']['coordinates']
        if len(pts) > 160: step = len(pts) / 160; pts = [pts[int(j * step)] for j in range(160)] + [pts[-1]]
        routes[f'{rep}|{a}'] = {'km': round(r['properties']['length']), 'path': [[round(x, 3), round(y, 3)] for x, y in pts]}
    except Exception as ex:
        failed += 1
    if i % 200 == 0: print('routed', i, 'of', len(pairs), round(time.time() - t0), 's', flush=True)
print('routes', len(routes), 'failed', failed)
sel = [x for x in sel if f"{x['p']}|{x['a']}" in routes]
for x in sel: x['km'] = routes[f"{x['p']}|{x['a']}"]['km']

out = {
    'year': 2019, 'unit': 'thousand tonnes', 'cargos': {k: v for k, v in cargos.items() if k != 'TOTAL'},
    'ports': [{'id': k, 'name': re.sub(r'\s*\(.*?\)', '', p['name']), 'cc': p['cc'], 'lng': p['xy'][0], 'lat': p['xy'][1], 'in': round(totals[k]['in']), 'out': round(totals[k]['out']),
               'cargo': {c: round(v) for c, v in totals[k]['cargo'].most_common(6)}} for k, p in located.items()],
    'anchors': {a: {'name': ANCHORS[a][2], 'label': partners.get(a, ANCHORS[a][2]), 'lng': ANCHORS[a][0], 'lat': ANCHORS[a][1]} for a in {x['a'] for x in sel}},
    'partners': {x['par']: partners[x['par']] for x in sel},
    'routes': {k: v['path'] for k, v in routes.items() if any(f"{x['p']}|{x['a']}" == k for x in sel)},
    'lanes': sel,
}
json.dump(out, open('public/data/sea.json', 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
print('ports out', len(out['ports']), 'lanes', len(out['lanes']), 'routes', len(out['routes']), 'bytes', os.path.getsize('public/data/sea.json'))
