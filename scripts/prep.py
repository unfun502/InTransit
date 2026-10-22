import csv, json, sys, zipfile, time, heapq, os, io
from collections import defaultdict
csv.field_size_limit(10**8)
DL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
TOP_ALL, TOP_X, TOP_TKM = 1800, 1500, 400   # biggest lanes overall, biggest cross-border lanes, biggest tonne-km lanes

nodes = {}
with open(f"{DL}/03_network-nodes.csv", newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        nodes[int(r['Network_Node_ID'])] = [round(float(r['Network_Node_X']),5), round(float(r['Network_Node_Y']),5)]
json.dump(nodes, open(f"{OUT}/nodes.json","w"), separators=(',',':'))

edges = []
with open(f"{DL}/04_network-edges.csv", newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        a, b = int(r['Network_Node_A_ID']), int(r['Network_Node_B_ID'])
        if a in nodes and b in nodes:
            edges.append([a, b, round(float(r['Distance']),1), int(float(r['Traffic_flow_trucks_2019'])), int(float(r['Traffic_flow_trucks_2030'])), int(r['Manually_Added'])])
json.dump(edges, open(f"{OUT}/network.json","w"), separators=(',',':'))

regions = {}
with open(f"{DL}/02_NUTS-3-Regions.csv", newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rid = int(r['ETISPlus_Zone_ID'])
        regions[rid] = {"id": rid, "name": r['Name'], "cc": r['Country'], "lng": round(float(r['Geometric_center_X']),4), "lat": round(float(r['Geometric_center_Y']),4), "node": int(r['Network_Node_ID']), "out19":0.0, "in19":0.0, "out30":0.0, "in30":0.0, "xout19":0.0, "xin19":0.0, "outkm":0.0}
cc_of = {k: v['cc'] for k, v in regions.items()}

country = defaultdict(lambda: [0.0,0.0,0.0,0.0])
heaps = {"all": [], "x": [], "tkm": []}
caps = {"all": TOP_ALL, "x": TOP_X, "tkm": TOP_TKM}
def push(name, key, item):
    h = heaps[name]
    if len(h) < caps[name]: heapq.heappush(h, (key, item[0], item))
    elif key > h[0][0]: heapq.heapreplace(h, (key, item[0], item))
region_top = defaultdict(list)
tot = [0.0,0.0,0.0]; n = 0
t0 = time.time()
with zipfile.ZipFile(f"{DL}/Trucktraffic.zip") as z:
    with z.open("01_Trucktrafficflow.csv") as raw:
        rd = csv.reader(io.TextIOWrapper(raw, encoding='utf-8', newline=''))
        next(rd)
        for row in rd:
            n += 1
            o, d = int(row[1]), int(row[3])
            dist = float(row[9]); t10, t19, t30 = float(row[13]), float(row[14]), float(row[15]); tr19 = float(row[11]); tr30 = float(row[12])
            tot[0]+=t10; tot[1]+=t19; tot[2]+=t30
            ro, rdst = regions.get(o), regions.get(d)
            if ro: ro['out19']+=t19; ro['out30']+=t30; ro['outkm']+=t19*dist
            if rdst: rdst['in19']+=t19; rdst['in30']+=t30
            co, cd = cc_of.get(o,'??'), cc_of.get(d,'??')
            xb = co != cd
            if xb:
                if ro: ro['xout19']+=t19
                if rdst: rdst['xin19']+=t19
            c = country[(co,cd)]; c[0]+=t19; c[1]+=t30; c[2]+=tr19; c[3]+=t10
            h = region_top[o]
            if len(h) < 8: heapq.heappush(h, (t19, d, dist))
            elif t19 > h[0][0]: heapq.heapreplace(h, (t19, d, dist))
            item = (n, [o, d, row[5], float(row[6]), float(row[7]), float(row[8]), dist, t10, t19, t30, tr19, tr30, 1 if xb else 0])
            push("all", t19, item)
            if xb: push("x", t19, item)
            push("tkm", t19*dist, item)
            if n % 250000 == 0: print(n, round(time.time()-t0), 's', flush=True)
print("rows", n, "tons", tot, round(time.time()-t0), 's')

seen = set(); flows = []
for name in ("all", "x", "tkm"):
    for key, idx, (_, r) in sorted(heaps[name], reverse=True):
        if idx in seen: continue
        seen.add(idx)
        path = [int(x) for x in r[2].strip('[]').split(',') if x.strip()]
        flows.append({"o": r[0], "d": r[1], "path": path, "d0": r[3], "dr": r[4], "d1": r[5], "dist": r[6], "t10": round(r[7]), "t19": round(r[8]), "t30": round(r[9]), "tr19": round(r[10]), "tr30": round(r[11]), "xb": r[12]})
flows.sort(key=lambda f: -f["t19"])
json.dump(flows, open(f"{OUT}/flows_top.json","w"), separators=(',',':'))

for r in regions.values():
    for k in ("out19","in19","out30","in30","xout19","xin19"): r[k] = round(r[k])
    r['avgkm'] = round(r['outkm']/r['out19']) if r['out19'] else 0
    del r['outkm']
json.dump(list(regions.values()), open(f"{OUT}/regions.json","w"), separators=(',',':'))
json.dump([{"o":k[0],"d":k[1],"t19":round(v[0]),"t30":round(v[1]),"tr19":round(v[2]),"t10":round(v[3])} for k,v in country.items()], open(f"{OUT}/country_flows.json","w"), separators=(',',':'))
json.dump({str(k): [[d, round(t), round(dist)] for t, d, dist in sorted(v, reverse=True)] for k, v in region_top.items()}, open(f"{OUT}/region_top.json","w"), separators=(',',':'))
json.dump({"rows": n, "tons10": round(tot[0]), "tons19": round(tot[1]), "tons30": round(tot[2]), "regions": len(regions), "edges": len(edges), "flows": len(flows)}, open(f"{OUT}/meta.json","w"))
print("done, flows kept:", len(flows))
