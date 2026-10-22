import csv, json, sys, math
DL, OUT = sys.argv[1], sys.argv[2]
edges = {}
with open(f"{DL}/04_network-edges.csv", newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        edges[int(r['Network_Edge_ID'])] = (int(r['Network_Node_A_ID']), int(r['Network_Node_B_ID']))
nodes = json.load(open(f"{OUT}/nodes.json"))
regions = {r['id']: r for r in json.load(open(f"{OUT}/regions.json"))}
flows = json.load(open(f"{OUT}/flows_top.json"))
bad = 0; single = 0
def d2(nid, r): x, y = nodes[str(nid)]; return (x - r['lng'])**2 + (y - r['lat'])**2
for fl in flows:
    es = [edges[e] for e in fl['path'] if e in edges]
    if not es: fl['path'] = []; bad += 1; continue
    seq = []
    if len(es) == 1:
        a, b = es[0]; o = regions[fl['o']]
        seq = [a, b] if d2(a, o) <= d2(b, o) else [b, a]; single += 1
    else:
        a, b = es[0]; n1 = set(es[1])
        start = b if a in n1 else a   # start is the node NOT shared with the next edge
        seq = [start, a if start == b else b]
        for a, b in es[1:]:
            last = seq[-1]
            if a == last: seq.append(b)
            elif b == last: seq.append(a)
            else: bad += 1; break  # broken chain
    fl['path'] = seq
json.dump(flows, open(f"{OUT}/flows_top.json", "w"), separators=(',', ':'))
ok = sum(1 for f in flows if len(f['path']) > 1)
print("flows", len(flows), "with paths", ok, "single-edge", single, "broken", bad, "avg nodes", round(sum(len(f['path']) for f in flows)/len(flows)))
