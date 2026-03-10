#!/usr/bin/env python3
"""Agent 4: Route Geometry (v3) - Non-siding tracks + Dijkstra corridor extraction"""
import sqlite3, csv, json, math, os, sys, heapq
from collections import defaultdict
try:
    from shapely import wkb
    from shapely.geometry import LineString, MultiLineString, Point, mapping
    from shapely.ops import linemerge, unary_union
except ImportError: print("ERROR: shapely"); sys.exit(1)
try:
    from pyproj import Transformer
except ImportError: print("ERROR: pyproj"); sys.exit(1)

BASE = "/Users/andreacrespo/CLAUDE/City101_ClaudeCode"
GPKG = os.path.join(BASE, "source/WORK copy/City101_TrainLines.gpkg")
STCSV = os.path.join(BASE, "datasets/transit/city101_service_frequency_v2.csv")
GACSV = os.path.join(BASE, "datasets/corridor_analysis/city101_ga_cost_corridor.csv")
ODIR = os.path.join(BASE, "output")
OGJN = os.path.join(ODIR, "corridor_rail_lines.geojson")
OCSV = os.path.join(ODIR, "corridor_station_distances.csv")
TBL = "swisstlm3d_chlv95ln02__tlm_eisenbahn_CITY101"
xf = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)
ST = 0.00006

def pgeo(b):
    if not b or len(b)<8 or b[:2]!=b'GP': return None
    fl=b[3]; et=(fl>>1)&0x07; es={0:0,1:32,2:48,3:48,4:64}.get(et,0)
    try: return wkb.loads(b[8+es:])
    except: return None
def txc(cs):
    r=[]
    for c in cs:
        lo,la=xf.transform(c[0],c[1])
        r.append((lo,la,c[2]) if len(c)>=3 else (lo,la))
    return r
def txg(g):
    if g.geom_type=='LineString': return LineString(txc(list(g.coords)))
    elif g.geom_type=='MultiLineString': return MultiLineString([LineString(txc(list(l.coords))) for l in g.geoms])
    return g
def ibb(g):
    a,b,c,d=g.bounds; return not(c<6.05 or a>7.10 or d<46.10 or b>46.55)
def els(g):
    if g.geom_type=='LineString': return [g] if len(g.coords)>=2 else []
    elif g.geom_type=='MultiLineString': return [l for l in g.geoms if len(l.coords)>=2]
    return []
def hav(a,b,c,d):
    R=6371000;p1,p2=math.radians(b),math.radians(d)
    dp=math.radians(d-b);dl=math.radians(c-a)
    x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R*2*math.atan2(math.sqrt(x),math.sqrt(1-x))
def lkm(l):
    c=list(l.coords);t=0
    for i in range(len(c)-1): t+=hav(c[i][0],c[i][1],c[i+1][0],c[i+1][1])
    return t/1000
def epk(p): return (round(p[0]/ST)*ST, round(p[1]/ST)*ST)

def badj(lines):
    """Adjacency graph: node -> [(line_idx, other_node, km)]"""
    ne = defaultdict(list)
    for i, l in enumerate(lines):
        c = list(l.coords)
        s, e = epk((c[0][0],c[0][1])), epk((c[-1][0],c[-1][1]))
        k = lkm(l)
        ne[s].append((i, e, k)); ne[e].append((i, s, k))
    return ne

def bcomp(lines):
    n=len(lines); ep=defaultdict(set)
    for i,l in enumerate(lines):
        c=list(l.coords)
        ep[epk((c[0][0],c[0][1]))].add(i); ep[epk((c[-1][0],c[-1][1]))].add(i)
    pa=list(range(n)); rk=[0]*n
    def fi(x):
        while pa[x]!=x: pa[x]=pa[pa[x]]; x=pa[x]
        return x
    def un(a,b):
        ra,rb=fi(a),fi(b)
        if ra==rb: return
        if rk[ra]<rk[rb]: ra,rb=rb,ra
        pa[rb]=ra
        if rk[ra]==rk[rb]: rk[ra]+=1
    for ids in ep.values():
        ids=list(ids)
        for j in range(1,len(ids)): un(ids[0],ids[j])
    co=defaultdict(list)
    for i in range(n): co[fi(i)].append(i)
    return co

def fnn(gn, lo, la):
    bn=None; bd=float('inf')
    for n in gn:
        d=math.sqrt((n[0]-lo)**2+(n[1]-la)**2)
        if d<bd: bd=d; bn=n
    return bn, bd

def dijk(gr, s, e):
    di={s:0}; pv={}; pl={}; pq=[(0,s)]; vi=set()
    while pq:
        d,u=heapq.heappop(pq)
        if u in vi: continue
        vi.add(u)
        if u==e: break
        for li,v,lk in gr.get(u,[]):
            nd=d+lk
            if nd<di.get(v,float('inf')):
                di[v]=nd; pv[v]=u; pl[v]=li; heapq.heappush(pq,(nd,v))
    if e not in pv and s!=e: return None, None, float('inf')
    pa=[]; ll=[]; n=e
    while n!=s: pa.append(n); ll.append(pl[n]); n=pv[n]
    pa.append(s); pa.reverse(); ll.reverse()
    return pa, ll, di.get(e, float('inf'))

def dal(line, frac):
    c=list(line.coords); td=frac*line.length; cu=0; rc=0
    for i in range(len(c)-1):
        sl=math.sqrt((c[i+1][0]-c[i][0])**2+(c[i+1][1]-c[i][1])**2)
        sr=hav(c[i][0],c[i][1],c[i+1][0],c[i+1][1])
        if cu+sl>=td:
            rm=td-cu; f=rm/sl if sl>0 else 0; rc+=f*sr; return rc/1000
        cu+=sl; rc+=sr
    return rc/1000

def main():
    print("="*80)
    print("AGENT 4: ROUTE GEOMETRY PROCESSING (v3)")
    print("="*80)
    print()

    gs = os.path.getsize(GPKG)
    print(f"STEP 1-2: Reading GeoPackage ({gs/1024/1024:.1f}MB)...")
    cn = sqlite3.connect(GPKG)
    cr = cn.execute(
        f'SELECT fid,geom,OBJEKTART,AUSSER_BETRIEB,MUSEUMSBAHN,STANDSEILBAHN,'
        f'ZAHNRADBAHN,ANSCHLUSSGLEIS,ACHSE_DKM,NAME,SHAPE_Length '
        f'FROM "{TBL}"')
    ft = []; pf = 0
    for r in cr:
        g = pgeo(r[1])
        if g is None: pf += 1; continue
        ft.append({'fid':r[0],'g':g,'oa':r[2],'ab':r[3],'mb':r[4],'sb':r[5],
                   'zb':r[6],'ag':r[7],'ad':r[8],'nm':r[9],'sl':r[10]})
    cn.close()
    print(f"  {len(ft)} features ({pf} failures)")

    # Filter: active, non-museum, non-funicular, NON-SIDING (AG=1)
    print("\nSTEP 3: Filtering to non-siding active rail...")
    f1 = [f for f in ft if f['ab']==1 and f['mb']==1 and f['sb']==1 and f['ag']==1]
    print(f"  Non-siding active rail: {len(f1)}")
    print(f"  Std: {sum(1 for f in f1 if f['oa']==0)}, Nar: {sum(1 for f in f1 if f['oa']==2)}")

    print("\nSTEP 4: LV95->WGS84...")
    for f in f1: f['gw'] = txg(f['g'])

    print("\nSTEP 5: Bbox...")
    ib = [f for f in f1 if ibb(f['gw'])]
    sib = [f for f in ib if f['oa']==0]; nib = [f for f in ib if f['oa']==2]
    print(f"  In bbox: {len(ib)} (std:{len(sib)}, nar:{len(nib)})")

    # Stations
    print("\nReading stations...")
    sraw = []
    with open(STCSV, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            n = row['name'].strip().strip('"')
            sraw.append({'name':n, 'sid':row['station_id'],
                        'lat':float(row['lat_wgs84']), 'lon':float(row['lon_wgs84']),
                        'pt':Point(float(row['lon_wgs84']), float(row['lat_wgs84']))})
    print(f"  {len(sraw)} stations")

    ga = {}; so = []
    with open(GACSV, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            nm = row['station'].strip().strip('"')
            ga[nm] = float(row['rail_km_est_from_geneva']); so.append(nm)
    print(f"  {len(ga)} GA entries (station order)")

    # Build graph
    print("\nSTEP 6: Building graph...")
    sl = []
    for f in sib:
        for l in els(f['gw']): sl.append(l)
    nl = []
    for f in nib:
        for l in els(f['gw']): nl.append(l)
    print(f"  Std lines: {len(sl)}, Nar lines: {len(nl)}")
    sg = badj(sl)
    print(f"  Std graph: {len(sg)} nodes")

    # Dijkstra corridor
    print("\nSTEP 7: Station-guided Dijkstra...")
    sn = {}; gn = list(sg.keys())
    for nm in so:
        sd = None
        for s in sraw:
            if s['name'] == nm: sd = s; break
        if not sd: continue
        nd, dd = fnn(gn, sd['lon'], sd['lat'])
        dm = hav(sd['lon'], sd['lat'], nd[0], nd[1]) if nd else float('inf')
        sn[nm] = {'node':nd, 'dm':dm, 'd':sd}

    rs = {k:v for k,v in sn.items() if v['dm'] < 2000}
    nrs = {k:v for k,v in sn.items() if v['dm'] >= 2000}
    print(f"  Rail stations: {len(rs)}")
    if nrs:
        print(f"  Non-rail (>2km): {len(nrs)}")
        for k,v in nrs.items(): print(f"    {k}: {v['dm']:.0f}m")
    orl = [s for s in so if s in rs]
    print(f"  Ordered: {len(orl)}")

    cls = set(); clines = []; tpk = 0; fld = []; ckm = [0.0]
    for i in range(len(orl)-1):
        s1, s2 = orl[i], orl[i+1]
        n1, n2 = rs[s1]['node'], rs[s2]['node']
        _, pls, pk = dijk(sg, n1, n2)
        if pls is None:
            fld.append((s1, s2)); ckm.append(ckm[-1])
        else:
            for li in pls:
                if li not in cls: cls.add(li); clines.append(sl[li])
            tpk += pk; ckm.append(ckm[-1] + pk)

    print(f"  Corridor: {len(clines)} segs, {tpk:.1f}km total Dijkstra path")
    if fld:
        print(f"  Failed {len(fld)} connections:")
        for s1,s2 in fld: print(f"    {s1} -> {s2}")

    # Merge
    print("\nSTEP 7b: Merging corridor...")
    mg = linemerge(clines)
    print(f"  linemerge: {mg.geom_type}")
    if mg.geom_type == 'MultiLineString':
        ps = sorted(mg.geoms, key=lambda g:g.length, reverse=True)
        print(f"  {len(ps)} pieces, stitching...")
        w = list(ps[0].coords); rm = list(ps[1:]); us = [False]*len(rm); sc = 0
        for _ in range(len(rm)):
            bi=-1; bd=float('inf'); be=bpe=None; ws=w[0]; we=w[-1]
            for j,p in enumerate(rm):
                if us[j]: continue
                pc = list(p.coords)
                for ref,w2,pt,pe in [(we,'e',pc[0],'s'),(we,'e',pc[-1],'e'),
                                      (ws,'s',pc[0],'s'),(ws,'s',pc[-1],'e')]:
                    d = math.sqrt((ref[0]-pt[0])**2+(ref[1]-pt[1])**2)
                    if d<bd: bd=d; bi=j; be=w2; bpe=pe
            if bi>=0 and bd<0.005:
                us[bi]=True; pc=list(rm[bi].coords); sc+=1
                if be=='e' and bpe=='s': w.extend(pc)
                elif be=='e' and bpe=='e': w.extend(reversed(pc))
                elif be=='s' and bpe=='s': w=list(reversed(pc))+w
                elif be=='s' and bpe=='e': w=pc+w
            else: break
        mg = LineString(w)
        print(f"  Stitched {sc}. {sum(1 for u in us if not u)} remaining.")

    mkm = lkm(mg) if mg.geom_type=='LineString' else sum(lkm(l) for l in mg.geoms)
    print(f"  Corridor length: {mkm:.1f}km")

    # Snap and distance
    print("\nSTEP 8-9: Station distances...")
    mlp = mg if mg.geom_type=='LineString' else max(mg.geoms, key=lambda g:g.length)
    all_lines = clines + nl

    sres = []
    for s in sraw:
        bd=float('inf'); bp=None; br="Unknown"
        for l in clines:
            try:
                d=l.project(s['pt']); p=l.interpolate(d); sd=s['pt'].distance(p)
                if sd<bd: bd=sd; bp=p; br="Main Line (Geneva-Villeneuve)"
            except: pass
        for l in nl:
            try:
                d=l.project(s['pt']); p=l.interpolate(d); sd=s['pt'].distance(p)
                if sd<bd: bd=sd; bp=p; br="Narrow gauge"
            except: pass
        sm = hav(s['lon'], s['lat'], bp.x, bp.y) if bp else float('inf')

        # Distance: Dijkstra cumulative if available
        dk = None
        if s['name'] in rs:
            try: dk = ckm[orl.index(s['name'])]
            except: pass
        if dk is None:
            da = mlp.project(s['pt']); fr = da/mlp.length if mlp.length>0 else 0
            dk = dal(mlp, fr)

        sres.append({'name':s['name'], 'sid':s['sid'], 'dk':dk, 'sm':sm,
                     'slat':bp.y if bp else s['lat'], 'slon':bp.x if bp else s['lon'], 'rt':br})

    sres.sort(key=lambda x: x['dk'])
    for i, sd in enumerate(sres):
        if i<len(sres)-1:
            sd['dtn'] = round(sres[i+1]['dk']-sd['dk'], 2); sd['ns'] = sres[i+1]['name']
        else: sd['dtn'] = None; sd['ns'] = None

    sds = [sd['sm'] for sd in sres]
    print(f"  Snap: min={min(sds):.0f}m, max={max(sds):.0f}m, mean={sum(sds)/len(sds):.0f}m")
    far = [sd for sd in sres if sd['sm']>1000]
    if far:
        print(f"  >1km: {len(far)}")
        for sd in far: print(f"    {sd['name']}: {sd['sm']:.0f}m ({sd['rt']})")
    print(f"  <100m: {sum(1 for sd in sres if sd['sm']<=100)}/{len(sres)}")
    print(f"  <300m: {sum(1 for sd in sres if sd['sm']<=300)}/{len(sres)}")
    print(f"  <500m: {sum(1 for sd in sres if sd['sm']<=500)}/{len(sres)}")
    print(f"  <1km: {sum(1 for sd in sres if sd['sm']<=1000)}/{len(sres)}")

    # Cross-validation
    print("\nSTEP 9b: Cross-validation...")
    dv = []
    for sd in sres:
        if sd['name'] in ga:
            e=ga[sd['name']]; a=sd['dk']; dv.append((sd['name'],e,a,a-e))
    if dv:
        ad = [abs(d[3]) for d in dv]
        print(f"  Matched {len(dv)}/{len(ga)}")
        print(f"  Mean abs: {sum(ad)/len(ad):.1f}km, Max: {max(ad):.1f}km, Min: {min(ad):.1f}km")
        ev=[d[1] for d in dv]; av=[d[2] for d in dv]
        me=sum(ev)/len(ev); ma=sum(av)/len(av)
        co=sum((e-me)*(a-ma) for e,a in zip(ev,av))
        se=math.sqrt(sum((e-me)**2 for e in ev)); sa=math.sqrt(sum((a-ma)**2 for a in av))
        cr=co/(se*sa) if se>0 and sa>0 else 0
        print(f"  Pearson r: {cr:.4f}")
        dv.sort(key=lambda d: abs(d[3]), reverse=True)
        print("  Top 5 deviations:")
        for n,e,a,d in dv[:5]: print(f"    {n}: exp {e:.1f}, got {a:.1f} ({d:+.1f})")

    # Route inventory
    print("\nRoute inventory...")
    ri = []
    mss = [sd['name'] for sd in sres if sd['rt']=="Main Line (Geneva-Villeneuve)" and sd['sm']<1000]
    ri.append({'name':"Main Line (Geneva-Villeneuve)", 'gauge':'standard',
               'lines':clines, 'lc':len(clines), 'km':mkm, 'sns':mss})

    nc = bcomp(nl) if nl else {}
    if nl:
        for cid,ll in sorted(nc.items(), key=lambda x:len(x[1]), reverse=True):
            cls2=[nl[i] for i in ll]; ck=sum(lkm(l) for l in cls2)
            if ck < 0.3: continue
            cu=unary_union(cls2); nb=[s['name'] for s in sraw if cu.distance(s['pt'])<0.005]
            def hs(ns,kw):
                for n in ns:
                    for k in kw:
                        if k.lower() in n.lower(): return True
                return False
            if hs(nb,['Montreux']) and ck>5: rn="MOB (Montreux-Oberland)"
            elif hs(nb,['Aigle']) and not hs(nb,['Montreux']): rn="TPC (Aigle region)"
            elif hs(nb,['Bex']): rn="BVB (Bex-Villars)"
            elif hs(nb,['Nyon']) and not hs(nb,['Montreux']): rn="NStCM (Nyon-St-Cergue)"
            elif hs(nb,['Lausanne-Flon']): rn="LEB (Lausanne-Echallens-Bercher)"
            elif nb: rn=f"Narrow gauge ({nb[0]} area)"
            else: rn=f"Narrow gauge ({ck:.1f}km)"
            ri.append({'name':rn,'gauge':'narrow','lines':cls2,'lc':len(ll),'km':ck,'sns':nb})

    ri.sort(key=lambda r: r['km'], reverse=True)
    for i,r in enumerate(ri):
        if r['km']>0.5 or r['sns']:
            print(f"  {i+1}. {r['name']}: {r['km']:.1f}km, {len(r['sns'])} stns ({r['gauge']})")

    # Write
    print("\nSTEP 10: Writing outputs...")
    fo = []
    for r in ri:
        if r['km']<0.1 and not r['sns']: continue
        rm2 = linemerge(r['lines'])
        if rm2.is_empty: continue
        if rm2.geom_type=='LineString':
            go=LineString([(c[0],c[1]) for c in rm2.coords])
        elif rm2.geom_type=='MultiLineString':
            go=MultiLineString([LineString([(c[0],c[1]) for c in l.coords]) for l in rm2.geoms])
        else: continue
        fo.append({'type':'Feature','geometry':mapping(go),'properties':{
            'type':'route','name':r['name'],'gauge':r['gauge'],
            'total_length_km':round(r['km'],2),'segment_count':r['lc'],
            'station_count':len(r['sns']),'station_names':', '.join(r['sns'])}})
    for sd in sres:
        fo.append({'type':'Feature','geometry':{'type':'Point','coordinates':[sd['slon'],sd['slat']]},
            'properties':{'type':'station','name':sd['name'],'station_id':sd['sid'],
            'line_name':sd['rt'],'distance_from_geneva_km':round(sd['dk'],2),
            'snap_distance_m':round(sd['sm'],1),'distance_to_next_km':sd['dtn'],
            'next_station':sd['ns']}})

    gj = {'type':'FeatureCollection',
          'crs':{'type':'name','properties':{'name':'urn:ogc:def:crs:OGC:1.3:CRS84'}},
          'features':fo}
    with open(OGJN, 'w', encoding='utf-8') as f: json.dump(gj, f, indent=2, ensure_ascii=False)
    gjs = os.path.getsize(OGJN)
    rc = sum(1 for feat in fo if feat['properties']['type']=='route')
    stc = sum(1 for feat in fo if feat['properties']['type']=='station')
    print(f"  {OGJN}: {gjs/1024:.0f}KB ({rc} routes, {stc} stations)")

    with open(OCSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['station_name','station_id','line_name','distance_from_geneva_km',
                     'distance_to_next_km','next_station','snap_distance_m','snapped_lat','snapped_lon'])
        for sd in sres:
            w.writerow([sd['name'],sd['sid'],sd['rt'],round(sd['dk'],2),
                        sd['dtn'] if sd['dtn'] is not None else '',sd['ns'] or '',
                        round(sd['sm'],1),round(sd['slat'],6),round(sd['slon'],6)])
    cs = os.path.getsize(OCSV)
    print(f"  {OCSV}: {cs/1024:.1f}KB ({len(sres)} rows)")

    # Summary
    print("\n"+"="*80); print("SUMMARY"); print("="*80)
    print(f"\nSource: GeoPackage ({gs/1024/1024:.1f}MB), {len(sraw)} stations, {len(ga)} validation")
    print(f"Pipeline: {len(ft)} raw -> {len(f1)} non-siding -> {len(ib)} bbox -> {len(sl)} std + {len(nl)} nar")
    print(f"\nRoute inventory:")
    print(f"  {'Name':<45} {'Len':>7} {'Seg':>5} {'Stn':>5} {'Gauge':<8}")
    print(f"  {'-'*45} {'-'*7} {'-'*5} {'-'*5} {'-'*8}")
    for r in ri:
        if r['km']>=0.5 or r['sns']:
            print(f"  {r['name']:<45} {r['km']:>6.1f}k {r['lc']:>4} {len(r['sns']):>4} {r['gauge']:<8}")
    print(f"\nSnap: <100m:{sum(1 for sd in sres if sd['sm']<=100)}/{len(sres)}, "
          f"<300m:{sum(1 for sd in sres if sd['sm']<=300)}/{len(sres)}, "
          f"<1km:{sum(1 for sd in sres if sd['sm']<=1000)}/{len(sres)}")
    print(f"Corridor: {mkm:.1f}km (expected ~101km), Dijkstra total: {tpk:.1f}km")
    print(f"Merged: {'LineString' if mg.geom_type=='LineString' else 'MultiLineString'}")
    print(f"\nDistance validation (first 15):")
    print(f"  {'Station':<35} {'Computed':>9} {'Expected':>9} {'Diff':>7}")
    ct=0
    for sd in sres:
        if sd['name'] in ga and ct<15:
            e=ga[sd['name']]; d2=sd['dk']-e
            print(f"  {sd['name']:<35} {sd['dk']:>8.1f} {e:>8.1f} {d2:>+6.1f}"); ct+=1
    if far:
        print(f"\n{len(far)} stations >1km from rail:")
        for sd in far: print(f"  * {sd['name']}: {sd['sm']:.0f}m ({sd['rt']})")
    print(f"\nOutputs: {OGJN} ({gjs/1024:.0f}KB), {OCSV} ({cs/1024:.1f}KB)")
    print("\nDone.")

if __name__ == '__main__': main()
