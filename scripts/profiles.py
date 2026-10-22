"""Stream the full Fraunhofer flow file once more and build per-highway-segment corridor profiles:
total 2019 tonnes using the segment, tonnes by origin country (top 6), and the top 5 lanes.
Also rewrites public/data/network.json with the edge ID as first element: [id, a, b, km, trucks19, trucks30, manual].
Usage: python -I scripts/profiles.py _dl/fraunhofer public/data
"""
import csv, json, sys, zipfile, io, heapq, time
from collections import defaultdict
csv.field_size_limit(10**8)
DL, OUT = sys.argv[1], sys.argv[2]
nodes = json.load(open(f"{OUT}/nodes.json"))
edges = []
with open(f"{DL}/04_network-edges.csv", newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        a, b = int(r['Network_Node_A_ID']), int(r['Network_Node_B_ID'])
        if str(a) in nodes and str(b) in nodes:
            edges.append([int(r['Network_Edge_ID']), a, b, round(float(r['Distance']), 1), int(float(r['Traffic_flow_trucks_2019'])), int(float(r['Traffic_flow_trucks_2030'])), int(r['Manually_Added'])])
json.dump(edges, open(f"{OUT}/network.json", "w"), separators=(',', ':'))
cc_of = {}
with open(f"{DL}/02_NUTS-3-Regions.csv", newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f): cc_of[int(r['ETISPlus_Zone_ID'])] = r['Country']

tot = defaultdict(float); bycc = defaultdict(lambda: defaultdict(float)); top = defaultdict(list)
n = 0; t0 = time.time()
with zipfile.ZipFile(f"{DL}/Trucktraffic.zip") as z, z.open("01_Trucktrafficflow.csv") as raw:
    rd = csv.reader(io.TextIOWrapper(raw, encoding='utf-8', newline='')); next(rd)
    for row in rd:
        n += 1
        t19 = float(row[14])
        if t19 <= 0: continue
        o, d = int(row[1]), int(row[3]); co = cc_of.get(o, '??')
        for e in row[5].strip('[]').split(','):
            e = e.strip()
            if not e: continue
            e = int(e)
            tot[e] += t19; bycc[e][co] += t19
            h = top[e]
            if len(h) < 5: heapq.heappush(h, (t19, o, d))
            elif t19 > h[0][0]: heapq.heapreplace(h, (t19, o, d))
        if n % 250000 == 0: print(n, round(time.time() - t0), 's', flush=True)
prof = {}
for e, t in tot.items():
    cc = sorted(bycc[e].items(), key=lambda kv: -kv[1])[:6]
    prof[str(e)] = {"t": round(t), "cc": [[c, round(v)] for c, v in cc], "top": [[o, d, round(v)] for v, o, d in sorted(top[e], reverse=True)]}
json.dump(prof, open(f"{OUT}/edge_profiles.json", "w"), separators=(',', ':'))
import os
print("rows", n, "edges with traffic", len(prof), "bytes", os.path.getsize(f"{OUT}/edge_profiles.json"), round(time.time() - t0), "s")
