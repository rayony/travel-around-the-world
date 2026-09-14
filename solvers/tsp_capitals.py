#!/usr/bin/env python3
"""Closed TSP on 196 capitals using great-circle (haversine) distance.

Start/end at Hong Kong (CityID 0). Heuristics only.

  python3 solvers/tsp_capitals.py --data data/capitals_0-195.csv
"""
from __future__ import annotations
import argparse, csv, json, math, time
from pathlib import Path
R_KM = 6371.0088

def haversine(lat1, lon1, lat2, lon2) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat, dlon = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * R_KM * math.asin(math.sqrt(min(1.0, max(0.0, a))))

def load_cities(path: Path):
    rows = []
    with path.open(encoding='utf-8') as f:
        for row in csv.DictReader(f):
            rows.append({'id': int(row['CityID']), 'nation': row.get('Independent Nation States w.r.t UN') or '', 'city': row['City / Capital City'], 'lat': float(row['Latitude (N+/S-)']), 'lon': float(row['Longitude (E+/W-)'])})
    rows.sort(key=lambda r: r['id'])
    return rows

def dist_matrix(cities):
    n = len(cities)
    D = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = haversine(cities[i]['lat'], cities[i]['lon'], cities[j]['lat'], cities[j]['lon'])
            D[i][j] = D[j][i] = d
    return D

def tour_len(D, tour):
    return sum(D[a][b] for a,b in zip(tour, tour[1:]))

def rotate_to_zero(tour):
    body = tour[:-1] if tour[0]==tour[-1] else list(tour)
    i = body.index(0)
    body = body[i:] + body[:i]
    return body + [0]

def valid(tour, n):
    body = tour[:-1]
    return tour[0]==tour[-1]==0 and len(body)==n and len(set(body))==n

def nearest_neighbour(D, start=0):
    unused = set(range(len(D))); unused.remove(start)
    tour = [start]; cur = start
    while unused:
        nxt = min(unused, key=lambda j: D[cur][j])
        tour.append(nxt); unused.remove(nxt); cur = nxt
    tour.append(start)
    return tour

def multi_start_nn(D):
    best, best_L, seed = None, 1e18, 0
    for s in range(len(D)):
        t = nearest_neighbour(D, s); L = tour_len(D, t)
        if L < best_L: best, best_L, seed = t, L, s
    return rotate_to_zero(best), seed, best_L

def farthest_insertion(D, start=0):
    n = len(D)
    far = max(range(n), key=lambda j: D[start][j] if j != start else -1)
    tour = [start, far, start]; used = {start, far}
    while len(used) < n:
        best_c, best_d = None, -1
        for c in range(n):
            if c in used: continue
            md = min(D[c][t] for t in used)
            if md > best_d: best_d, best_c = md, c
        pos, best_inc = 1, 1e18
        for i in range(len(tour)-1):
            inc = D[tour[i]][best_c] + D[best_c][tour[i+1]] - D[tour[i]][tour[i+1]]
            if inc < best_inc: best_inc, pos = inc, i+1
        tour.insert(pos, best_c); used.add(best_c)
    return rotate_to_zero(tour)

def two_opt(D, tour, max_passes=40):
    tour = list(tour)
    if tour[0] != tour[-1]: tour.append(tour[0])
    m = len(tour)-1; improved, passes = True, 0
    while improved and passes < max_passes:
        improved = False; passes += 1
        for i in range(1, m-1):
            a, b = tour[i-1], tour[i]
            for j in range(i+1, m):
                c, d = tour[j], tour[j+1]
                if D[a][c] + D[b][d] - D[a][b] - D[c][d] < -1e-6:
                    tour[i:j+1] = reversed(tour[i:j+1]); improved = True; break
            if improved: break
    return rotate_to_zero(tour)

def or_opt(D, tour, max_passes=15):
    tour = list(tour)
    if tour[0] != tour[-1]: tour.append(tour[0])
    n = len(tour)-1; improved, passes = True, 0; L = tour_len(D, tour)
    while improved and passes < max_passes:
        improved = False; passes += 1
        for length in (1, 2, 3):
            for i in range(1, n-length):
                a, b = tour[i-1], tour[i]
                c, d = tour[i+length-1], tour[i+length]
                chunk = tour[i:i+length]
                rest = tour[:i] + tour[i+length:-1]
                base = L - D[a][b] - D[c][d] + D[a][d]
                for p, x in enumerate(rest):
                    y = rest[(p+1) % len(rest)]
                    nL = base - D[x][y] + D[x][b] + D[c][y]
                    if nL + 1e-6 < L:
                        nt = rest[:p+1] + chunk + rest[p+1:]; nt = nt + [nt[0]]
                        if valid(rotate_to_zero(nt), len(D)):
                            tour = rotate_to_zero(nt); L = tour_len(D, tour); improved = True; break
                if improved: break
            if improved: break
    return tour

def three_opt_once(D, tour):
    body = tour[:-1]; n = len(body); L = tour_len(D, body + [body[0]])
    def seg(u, v): return body[u:v] if u < v else body[u:] + body[:v]
    for i in range(n-2):
        a, b = body[i], body[(i+1)%n]
        for j in range(i+2, n if i else n-1):
            c, d = body[j], body[(j+1)%n]
            for k in range(j+2, (n if i else n-1)):
                e, f = body[k], body[(k+1)%n]
                d0 = D[a][b] + D[c][d] + D[e][f]
                cases = [(D[a][c]+D[b][d]+D[e][f],'2ij'),(D[a][b]+D[c][e]+D[d][f],'2jk'),(D[a][e]+D[d][b]+D[c][f],'2ik'),(D[a][d]+D[e][b]+D[c][f],'3p'),(D[a][c]+D[b][e]+D[d][f],'3q'),(D[a][d]+D[e][c]+D[b][f],'3r'),(D[a][e]+D[d][c]+D[b][f],'3s')]
                best = min(cases, key=lambda x: x[0])
                if best[0] + 1e-6 >= d0: continue
                A, B, C = seg((i+1)%n,(j+1)%n), seg((j+1)%n,(k+1)%n), seg((k+1)%n,(i+1)%n)
                kind = best[1]
                if kind=='2ij': new = list(reversed(A))+B+C
                elif kind=='2jk': new = A+list(reversed(B))+C
                elif kind=='2ik': new = list(reversed(A+B))+C
                elif kind=='3p': new = B+list(reversed(A))+C
                elif kind=='3q': new = list(reversed(A))+list(reversed(B))+C
                elif kind=='3r': new = B+A+C
                else: new = list(reversed(B))+A+C
                if len(new)!=n or len(set(new))!=n: continue
                nL = tour_len(D, new+[new[0]])
                if nL + 1e-6 < L: return rotate_to_zero(new+[new[0]])
    return rotate_to_zero(tour)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default='data/capitals_0-195.csv')
    ap.add_argument('--out', default='output/tours.json')
    args = ap.parse_args()
    cities = load_cities(Path(args.data)); n = len(cities); D = dist_matrix(cities); results = {}
    def record(key, name, tour, sec):
        tour = rotate_to_zero(tour); assert valid(tour, n), key
        results[key] = {'name': name, 'km': round(tour_len(D, tour), 3), 'sec': round(sec, 3), 'tour': tour}
        print(f"{results[key]['km']:10.1f} km  {sec:6.2f}s  {name}")
    t0 = time.time(); record('nn_hk', 'Nearest neighbour from Hong Kong', nearest_neighbour(D, 0), time.time()-t0)
    t0 = time.time(); t, seed, _ = multi_start_nn(D); record('nn_multi', f'NN multi-start (best seed {seed}), rotated to HK', t, time.time()-t0)
    t0 = time.time(); fi = farthest_insertion(D, 0); record('fi', 'Farthest insertion', fi, time.time()-t0)
    t0 = time.time(); record('fi2', 'Farthest insertion + 2-opt', two_opt(D, fi), time.time()-t0)
    t0 = time.time(); t2 = two_opt(D, t); record('two_opt', '2-opt on multi-start NN', t2, time.time()-t0)
    t0 = time.time(); ot = two_opt(D, or_opt(D, t2)); record('oropt', '2-opt + Or-opt + 2-opt polish', ot, time.time()-t0)
    t0 = time.time(); record('three', '3-opt first-improvement on Or-opt (valid cycle only)', two_opt(D, three_opt_once(D, ot)), time.time()-t0)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'radius_km': R_KM, 'n': n, 'results': results}), encoding='utf-8')
    print('wrote', out)

if __name__ == '__main__':
    main()
