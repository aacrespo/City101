#!/usr/bin/env python3
"""Agent 4: Route Geometry (v4) - Mainline spine + bridge edges + calibrated distances.

Approach:
1. Build corridor geometry using Dijkstra with bridge edges (for visualization)
2. Compute raw along-corridor projection for all stations
3. Calibrate the projection using GA reference distances at known spine stations
   (piecewise linear interpolation between calibration points)
4. This gives accurate distances even though the corridor geometry has extra length
"""
import sqlite3, csv, json, math, os, sys, heapq
from collections import defaultdict
try:
    from shapely import wkb
    from shapely.geometry import LineString, MultiLineString, Point, mapping
    from shapely.ops import linemerge, unary_union
except ImportError: print("ERROR: shapely not installed"); sys.exit(1)
try:
    from pyproj import Transformer
except ImportError: print("ERROR: pyproj not installed"); sys.exit(1)

BASE = "/Users/andreacrespo/CLAUDE/City101_ClaudeCode"
GPKG = os.path.join(BASE, "source/WORK copy/City101_TrainLines.gpkg")
STCSV = os.path.join(BASE, "datasets/transit/city101_service_frequency_v2.csv")
GACSV = os.path.join(BASE, "datasets/corridor_analysis/city101_ga_cost_corridor.csv")
ODIR = os.path.join(BASE, "output")
OGJN = os.path.join(ODIR, "corridor_rail_lines.geojson")
OCSV = os.path.join(ODIR, "corridor_station_distances.csv")
TBL = "swisstlm3d_chlv95ln02__tlm_eisenbahn_CITY101"
xf = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)
QS = 0.00006
BRIDGE_THRESHOLD = 0.003

MAINLINE_SPINE = [
    "Geneve", "Geneve-Secheron", "Genthod-Bellevue", "Versoix",
    "Mies", "Tannay", "Coppet", "Nyon", "Gland", "Rolle",
    "Allaman", "St-Prex", "Morges", "Lonay-Preverenges",
    "Denges-Echandens", "Bussigny", "Renens VD", "Prilly-Malley",
    "Lausanne", "La Conversion", "Bossiere", "Cully",
    "Grandvaux", "Epesses", "Puidoux", "Rivaz",
    "St-Saphorin (Lavaux), gare", "Vevey", "La Tour-de-Peilz",
    "Burier", "Clarens", "Montreux", "Territet", "Villeneuve VD",
    "Aigle", "Bex",
]

BRANCH_STATIONS = {
    "Geneve-Eaux-Vives": "CEVA",
    "Geneve-Champel": "CEVA",
    "Lancy-Pont-Rouge": "CEVA",
    "Geneve-Aeroport": "Airport branch",
    "Vernier, Blandonnet": "Tram/bus",
    "Lancy-Bachet": "CEVA junction",
    "Founex, est": "Bus stop",
    "Prangins, Les Aberiaux": "Bus stop",
    "Begnins, poste": "Bus stop",
    "Perroy, Couronnette": "Bus stop",
    "Aubonne, gare": "Bus stop",
    "Lausanne-Flon": "LEB narrow gauge",
    "Palezieux": "Fribourg branch",
}


def normalize_name(n):
    n = n.strip().strip('"')
    reps = {'\xe8':'e','\xe9':'e','\xea':'e','\xeb':'e',
            '\xe0':'a','\xe2':'a','\xe4':'a',
            '\xf9':'u','\xfb':'u','\xfc':'u',
            '\xee':'i','\xef':'i','\xf4':'o','\xf6':'o','\xe7':'c'}
    for old, new in reps.items(): n = n.replace(old, new)
    return n

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

def hav(lon1,lat1,lon2,lat2):
    R=6371000;p1,p2=math.radians(lat1),math.radians(lat2)
    dp=math.radians(lat2-lat1);dl=math.radians(lon2-lon1)
    x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R*2*math.atan2(math.sqrt(x),math.sqrt(1-x))

def lkm(line):
    c=list(line.coords);t=0
    for i in range(len(c)-1): t+=hav(c[i][0],c[i][1],c[i+1][0],c[i+1][1])
    return t/1000

def epk(p): return (round(p[0]/QS)*QS, round(p[1]/QS)*QS)

def badj(lines):
    ne=defaultdict(list)
    for i,l in enumerate(lines):
        c=list(l.coords)
        s,e=epk((c[0][0],c[0][1])),epk((c[-1][0],c[-1][1]))
        k=lkm(l)
        ne[s].append((i,e,k)); ne[e].append((i,s,k))
    return ne

def add_bridge_edges(graph, threshold=BRIDGE_THRESHOLD):
    nodes=list(graph.keys())
    parent={}
    def find(x):
        if x not in parent: parent[x]=x
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[ra]=rb
    for n in nodes:
        for _,other,_ in graph[n]: union(n,other)
    comp_nodes=defaultdict(list)
    for n in nodes: comp_nodes[find(n)].append(n)
    if len(comp_nodes)<=1: return 0
    bc=0; comp_list=list(comp_nodes.items())
    for ci in range(len(comp_list)):
        for cj in range(ci+1,len(comp_list)):
            _,ni=comp_list[ci]; _,nj=comp_list[cj]
            best_d=float('inf'); best_pair=None
            for a in ni:
                for b in nj:
                    d=math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
                    if d<best_d: best_d=d; best_pair=(a,b)
            if best_d<threshold and best_pair:
                km=hav(best_pair[0][0],best_pair[0][1],best_pair[1][0],best_pair[1][1])/1000
                graph[best_pair[0]].append((-1,best_pair[1],km))
                graph[best_pair[1]].append((-1,best_pair[0],km))
                bc+=1; dm=km*1000
                union(best_pair[0],best_pair[1])
                print(f"    Bridge: {dm:.0f}m (comp {len(ni)} <-> {len(nj)} nodes)")
    return bc

def bcomp(lines):
    n=len(lines);ep=defaultdict(set)
    for i,l in enumerate(lines):
        c=list(l.coords)
        ep[epk((c[0][0],c[0][1]))].add(i); ep[epk((c[-1][0],c[-1][1]))].add(i)
    pa=list(range(n));rk=[0]*n
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

def fnn(gn,lo,la):
    bn=None;bd=float('inf')
    for n in gn:
        d=math.sqrt((n[0]-lo)**2+(n[1]-la)**2)
        if d<bd: bd=d; bn=n
    return bn,bd

def dijk(gr,s,e):
    di={s:0};pv={};pl={};pq=[(0,s)];vi=set()
    while pq:
        d,u=heapq.heappop(pq)
        if u in vi: continue
        vi.add(u)
        if u==e: break
        for li,v,lk in gr.get(u,[]):
            nd=d+lk
            if nd<di.get(v,float('inf')):
                di[v]=nd;pv[v]=u;pl[v]=li;heapq.heappush(pq,(nd,v))
    if e not in pv and s!=e: return None,None,float('inf')
    pa=[];ll=[];n=e
    while n!=s: pa.append(n);ll.append(pl[n]);n=pv[n]
    pa.append(s);pa.reverse();ll.reverse()
    return pa,ll,di.get(e,float('inf'))

def raw_proj_km(line, point):
    """Raw along-line distance in km (haversine-based) to the projection of a point."""
    proj=line.project(point); total=line.length
    if total==0: return 0.0
    frac=proj/total; c=list(line.coords)
    cum_e=0.0;cum_h=0.0;target=frac*total
    for i in range(len(c)-1):
        se=math.sqrt((c[i+1][0]-c[i][0])**2+(c[i+1][1]-c[i][1])**2)
        sh=hav(c[i][0],c[i][1],c[i+1][0],c[i+1][1])
        if cum_e+se>=target:
            rem=target-cum_e; f=rem/se if se>0 else 0
            return (cum_h+f*sh)/1000
        cum_e+=se; cum_h+=sh
    return cum_h/1000

def calibrate_distance(raw_km, cal_points):
    """Piecewise linear interpolation using calibration points.
    cal_points: sorted list of (raw_km, ga_km) tuples.
    """
    if not cal_points: return raw_km
    if raw_km <= cal_points[0][0]: 
        # Below first calibration point: extrapolate from first segment
        if len(cal_points) >= 2:
            r0,g0 = cal_points[0]
            r1,g1 = cal_points[1]
            if r1 != r0:
                return g0 + (raw_km - r0) * (g1 - g0) / (r1 - r0)
        return cal_points[0][1] + (raw_km - cal_points[0][0])
    if raw_km >= cal_points[-1][0]:
        # Above last calibration point: extrapolate from last segment
        if len(cal_points) >= 2:
            r0,g0 = cal_points[-2]
            r1,g1 = cal_points[-1]
            if r1 != r0:
                return g1 + (raw_km - r1) * (g1 - g0) / (r1 - r0)
        return cal_points[-1][1] + (raw_km - cal_points[-1][0])
    # Find bracketing calibration points
    for i in range(len(cal_points)-1):
        r0,g0 = cal_points[i]
        r1,g1 = cal_points[i+1]
        if r0 <= raw_km <= r1:
            if r1 == r0: return g0
            t = (raw_km - r0) / (r1 - r0)
            return g0 + t * (g1 - g0)
    return raw_km

def snap_to_lines(pt, lines):
    bd=float('inf');bp=None;bi=-1
    for i,l in enumerate(lines):
        try:
            d=l.project(pt);p=l.interpolate(d);sd=pt.distance(p)
            if sd<bd: bd=sd;bp=p;bi=i
        except: pass
    dm=hav(pt.x,pt.y,bp.x,bp.y) if bp else float('inf')
    return bp,dm,bi


def main():
    print("="*80)
    print("AGENT 4: ROUTE GEOMETRY PROCESSING (v4)")
    print("Mainline spine + bridge edges + calibrated distances")
    print("="*80)
    print()

    gs=os.path.getsize(GPKG)
    print(f"STEP 1-2: Reading GeoPackage ({gs/1024/1024:.1f}MB)...")
    cn=sqlite3.connect(GPKG)
    cr=cn.execute(
        f'SELECT fid,geom,OBJEKTART,AUSSER_BETRIEB,MUSEUMSBAHN,STANDSEILBAHN,'
        f'ZAHNRADBAHN,ANSCHLUSSGLEIS,ACHSE_DKM,NAME,SHAPE_Length '
        f'FROM "{TBL}"')
    ft=[];pf=0
    for r in cr:
        g=pgeo(r[1])
        if g is None: pf+=1; continue
        ft.append({'fid':r[0],'g':g,'oa':r[2],'ab':r[3],'mb':r[4],
                   'sb':r[5],'zb':r[6],'ag':r[7],'ad':r[8],'nm':r[9],'sl':r[10]})
    cn.close()
    print(f"  {len(ft)} features ({pf} failures)")

    print("\nSTEP 3: Filter non-siding active rail...")
    f1=[f for f in ft if f['ab']==1 and f['mb']==1 and f['sb']==1 and f['ag']==1]
    print(f"  {len(f1)} features (std:{sum(1 for f in f1 if f['oa']==0)}, nar:{sum(1 for f in f1 if f['oa']==2)})")

    print("\nSTEP 4: LV95 -> WGS84...")
    for f in f1: f['gw']=txg(f['g'])

    print("\nSTEP 5: Bbox...")
    ib=[f for f in f1 if ibb(f['gw'])]
    sib=[f for f in ib if f['oa']==0]; nib=[f for f in ib if f['oa']==2]
    print(f"  In bbox: {len(ib)} (std:{len(sib)}, nar:{len(nib)})")
    std_lines=[]
    for f in sib:
        for l in els(f['gw']): std_lines.append(l)
    nar_lines=[]
    for f in nib:
        for l in els(f['gw']): nar_lines.append(l)
    print(f"  Lines: {len(std_lines)} std, {len(nar_lines)} nar")

    print("\nReading stations...")
    sraw=[]
    with open(STCSV,'r',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            n=row['name'].strip().strip('"')
            sraw.append({'name':n,'sid':row['station_id'],
                        'lat':float(row['lat_wgs84']),'lon':float(row['lon_wgs84']),
                        'pt':Point(float(row['lon_wgs84']),float(row['lat_wgs84']))})
    print(f"  {len(sraw)} stations")
    ga_data={};ga_order=[]
    with open(GACSV,'r',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            nm=row['station'].strip().strip('"')
            ga_data[nm]={'rail_km':float(row['rail_km_est_from_geneva']),
                        'lat':float(row['lat_wgs84']),'lon':float(row['lon_wgs84'])}
            ga_order.append(nm)
    print(f"  {len(ga_data)} GA cost entries")

    print("\nSTEP 6: Graph + bridge edges...")
    graph=badj(std_lines)
    print(f"  {len(graph)} nodes, adding bridges...")
    bc=add_bridge_edges(graph, BRIDGE_THRESHOLD)
    print(f"  {bc} bridges added")
    graph_nodes=list(graph.keys())

    print("\nSTEP 7: Mainline spine Dijkstra...")
    spine_matched=[]
    spine_failed=[]
    for spine_name in MAINLINE_SPINE:
        sn=normalize_name(spine_name)
        sd=None
        for s in sraw:
            if normalize_name(s['name'])==sn: sd=s; break
        if sd is None:
            for gn,gd in ga_data.items():
                if normalize_name(gn)==sn:
                    sd={'name':gn,'sid':'','lat':gd['lat'],'lon':gd['lon'],
                        'pt':Point(gd['lon'],gd['lat'])}; break
        if sd is None: spine_failed.append(spine_name); continue
        nd,dd=fnn(graph_nodes, sd['lon'], sd['lat'])
        dm=hav(sd['lon'],sd['lat'],nd[0],nd[1]) if nd else float('inf')
        max_snap = 15000 if spine_name in ("Aigle","Bex") else 5000
        if dm>max_snap: spine_failed.append(f"{spine_name} ({dm:.0f}m)"); continue
        spine_matched.append({'spine_name':spine_name,'station':sd,'node':nd,'snap_m':dm})

    print(f"  Matched: {len(spine_matched)}/{len(MAINLINE_SPINE)}")
    if spine_failed: print(f"  Failed: {spine_failed}")

    corridor_idx=set(); corridor_lines_list=[]; failed_conn=[]
    for i in range(len(spine_matched)-1):
        s1=spine_matched[i]; s2=spine_matched[i+1]
        _,pls,pk=dijk(graph,s1['node'],s2['node'])
        if pls is None:
            failed_conn.append((s1['spine_name'],s2['spine_name']))
            print(f"  FAILED: {s1['spine_name']} -> {s2['spine_name']}")
        else:
            for li in pls:
                if li>=0 and li not in corridor_idx:
                    corridor_idx.add(li); corridor_lines_list.append(std_lines[li])
    print(f"  Corridor: {len(corridor_lines_list)} segs, {len(failed_conn)} failed")

    print("\nSTEP 7b: Merging...")
    merged=linemerge(corridor_lines_list)
    if merged.geom_type=='MultiLineString':
        pieces=sorted(merged.geoms, key=lambda g:g.length, reverse=True)
        print(f"  {len(pieces)} pieces, stitching...")
        work=list(pieces[0].coords); rm=list(pieces[1:]); us=[False]*len(rm); sc=0
        for _ in range(len(rm)):
            bi2=-1;bd2=float('inf');be2=bpe2=None;ws=work[0];we=work[-1]
            for j,p in enumerate(rm):
                if us[j]: continue
                pc=list(p.coords)
                for ref,w2,pt2,pe in [(we,'e',pc[0],'s'),(we,'e',pc[-1],'e'),
                                       (ws,'s',pc[0],'s'),(ws,'s',pc[-1],'e')]:
                    d2=math.sqrt((ref[0]-pt2[0])**2+(ref[1]-pt2[1])**2)
                    if d2<bd2: bd2=d2;bi2=j;be2=w2;bpe2=pe
            if bi2>=0 and bd2<0.01:
                us[bi2]=True;pc=list(rm[bi2].coords);sc+=1
                if be2=='e' and bpe2=='s': work.extend(pc)
                elif be2=='e' and bpe2=='e': work.extend(reversed(pc))
                elif be2=='s' and bpe2=='s': work=list(reversed(pc))+work
                elif be2=='s' and bpe2=='e': work=pc+work
            else: break
        merged=LineString(work)
        print(f"  Stitched {sc}. {sum(1 for u in us if not u)} remaining.")
    corridor_km=lkm(merged) if merged.geom_type=='LineString' else sum(lkm(l) for l in merged.geoms)
    print(f"  Corridor: {corridor_km:.1f}km")

    # Orient west->east
    if merged.geom_type=='LineString':
        coords=list(merged.coords)
        if coords[0][0]>coords[-1][0]:
            coords.reverse(); merged=LineString(coords)
            print("  Oriented west->east")

    # STEP 8: Raw projections + calibration
    print("\nSTEP 8: Raw projections + distance calibration...")

    # Get raw projections for all stations
    raw_projs = {}
    for s in sraw:
        rk = raw_proj_km(merged, s['pt'])
        raw_projs[s['name']] = rk

    # Build calibration points: spine stations that are ON the mainline
    # (have GA reference distances and project well onto the corridor)
    # Use only mainline spine stations (not branch stations) for calibration
    cal_points = []
    for spine_name in MAINLINE_SPINE:
        sn = normalize_name(spine_name)
        # Find the actual station name
        actual_name = None
        for s in sraw:
            if normalize_name(s['name']) == sn:
                actual_name = s['name']; break
        if actual_name is None:
            for gn in ga_data:
                if normalize_name(gn) == sn:
                    actual_name = gn; break
        if actual_name and actual_name in ga_data and actual_name in raw_projs:
            ga_km = ga_data[actual_name]['rail_km']
            raw_km = raw_projs[actual_name]
            cal_points.append((raw_km, ga_km, actual_name))

    # Sort by raw_km and remove duplicates / non-monotonic points
    cal_points.sort(key=lambda x: x[0])
    # Ensure monotonic: ga_km should increase with raw_km
    clean_cal = []
    for rk, gk, nm in cal_points:
        if not clean_cal or gk >= clean_cal[-1][1]:
            clean_cal.append((rk, gk))
        # else: skip this point (non-monotonic, probably a branch)
    
    print(f"  Calibration points: {len(clean_cal)}/{len(cal_points)} (monotonic)")
    print(f"  Raw range: {clean_cal[0][0]:.1f} - {clean_cal[-1][0]:.1f}km")
    print(f"  GA range: {clean_cal[0][1]:.1f} - {clean_cal[-1][1]:.1f}km")

    # Apply calibration to all stations
    results = []
    for s in sraw:
        sn2 = normalize_name(s['name'])
        is_branch = False; branch_type = None
        for bn, bt in BRANCH_STATIONS.items():
            if normalize_name(bn) == sn2: is_branch = True; branch_type = bt; break

        # Snap
        bp_c,dm_c,_ = snap_to_lines(s['pt'], corridor_lines_list)
        bp_n,dm_n,_ = snap_to_lines(s['pt'], nar_lines) if nar_lines else (None,float('inf'),-1)
        if dm_c <= dm_n or dm_n == float('inf'):
            snap_pt=bp_c; snap_dm=dm_c; route="Main Line (Geneva-Villeneuve)"
        else:
            snap_pt=bp_n; snap_dm=dm_n; route="Narrow gauge"

        # Distance: calibrated projection
        raw_km = raw_projs[s['name']]
        cal_km = calibrate_distance(raw_km, clean_cal)

        ga_ref = ga_data[s['name']]['rail_km'] if s['name'] in ga_data else None

        results.append({'name':s['name'],'sid':s['sid'],
                       'dist_km':cal_km, 'raw_km':raw_km,
                       'ga_ref_km':ga_ref,'snap_m':snap_dm,
                       'snap_lat':snap_pt.y if snap_pt else s['lat'],
                       'snap_lon':snap_pt.x if snap_pt else s['lon'],
                       'route':route,'is_branch':is_branch,'branch_type':branch_type})

    results.sort(key=lambda x: x['dist_km'])
    for i,sd in enumerate(results):
        if i<len(results)-1:
            sd['dist_to_next']=round(results[i+1]['dist_km']-sd['dist_km'],2)
            sd['next_station']=results[i+1]['name']
        else:
            sd['dist_to_next']=None; sd['next_station']=None

    # STEP 9: Quality
    print("\nSTEP 9: Quality assessment...")
    snaps=[sd['snap_m'] for sd in results]
    print(f"  Snap: min={min(snaps):.0f}m max={max(snaps):.0f}m mean={sum(snaps)/len(snaps):.0f}m")
    print(f"  <100m:{sum(1 for d in snaps if d<=100)}/{len(results)}, "
          f"<300m:{sum(1 for d in snaps if d<=300)}/{len(results)}, "
          f"<1km:{sum(1 for d in snaps if d<=1000)}/{len(results)}")

    far=[sd for sd in results if sd['snap_m']>1000]
    if far:
        print(f"  >1km ({len(far)}):")
        for sd in far: print(f"    {sd['name']}: {sd['snap_m']:.0f}m")

    print(f"\n  Distance validation (calibrated):")
    devs=[]
    for sd in results:
        if sd['ga_ref_km'] is not None:
            diff=sd['dist_km']-sd['ga_ref_km']
            devs.append((sd['name'],sd['ga_ref_km'],sd['dist_km'],diff))
    if devs:
        ad=[abs(d[3]) for d in devs]
        print(f"  Matched: {len(devs)}")
        print(f"  Mean abs dev: {sum(ad)/len(ad):.1f}km, Median: {sorted(ad)[len(ad)//2]:.1f}km, Max: {max(ad):.1f}km")
        ev=[d[1] for d in devs]; av=[d[2] for d in devs]
        me=sum(ev)/len(ev); ma=sum(av)/len(av)
        co2=sum((e-me)*(a-ma) for e,a in zip(ev,av))
        se2=math.sqrt(sum((e-me)**2 for e in ev)); sa2=math.sqrt(sum((a-ma)**2 for a in av))
        pr=co2/(se2*sa2) if se2>0 and sa2>0 else 0
        print(f"  Pearson r: {pr:.4f}")

        print(f"\n  {'Station':<35} {'Calibrated':>10} {'Expected':>9} {'Diff':>7} {'Raw':>7}")
        print(f"  {'-'*35} {'-'*10} {'-'*9} {'-'*7} {'-'*7}")
        for sd in results:
            if sd['ga_ref_km'] is not None:
                diff=sd['dist_km']-sd['ga_ref_km']
                flag=" *" if abs(diff)>3 else ""
                print(f"  {sd['name']:<35} {sd['dist_km']:>9.1f} {sd['ga_ref_km']:>8.1f} {diff:>+6.1f} {sd['raw_km']:>6.1f}{flag}")

    # Route inventory
    print("\n  Route inventory:")
    ri=[]
    msns=[sd['name'] for sd in results if sd['route']=="Main Line (Geneva-Villeneuve)" and sd['snap_m']<1000]
    ri.append({'name':"Main Line (Geneva-Villeneuve)",'gauge':'standard',
               'lines':corridor_lines_list,'lc':len(corridor_lines_list),'km':corridor_km,'sns':msns})
    if nar_lines:
        nc=bcomp(nar_lines)
        for cid,ll in sorted(nc.items(), key=lambda x:len(x[1]), reverse=True):
            cls2=[nar_lines[i] for i in ll]; ck=sum(lkm(l) for l in cls2)
            if ck<0.3: continue
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

    ri.sort(key=lambda r:r['km'], reverse=True)
    print(f"  {'Name':<45} {'Len':>8} {'Seg':>5} {'Stn':>5}")
    for r in ri:
        if r['km']>=0.5 or r['sns']:
            print(f"  {r['name']:<45} {r['km']:>7.1f}k {r['lc']:>4} {len(r['sns']):>4}")

    # STEP 10: Write
    print("\nSTEP 10: Writing outputs...")
    features=[]
    for r in ri:
        if r['km']<0.1 and not r['sns']: continue
        rm2=linemerge(r['lines'])
        if rm2.is_empty: continue
        if rm2.geom_type=='LineString':
            go=LineString([(c[0],c[1]) for c in rm2.coords])
        elif rm2.geom_type=='MultiLineString':
            go=MultiLineString([LineString([(c[0],c[1]) for c in l.coords]) for l in rm2.geoms])
        else: continue
        features.append({'type':'Feature','geometry':mapping(go),'properties':{
            'type':'route','name':r['name'],'gauge':r['gauge'],
            'total_length_km':round(r['km'],2),'segment_count':r['lc'],
            'station_count':len(r['sns']),'station_names':', '.join(r['sns'])}})

    for sd in results:
        features.append({'type':'Feature','geometry':{'type':'Point',
            'coordinates':[round(sd['snap_lon'],6),round(sd['snap_lat'],6)]},
            'properties':{'type':'station','name':sd['name'],'station_id':sd['sid'],
            'line_name':sd['route'],'distance_from_geneva_km':round(sd['dist_km'],2),
            'ga_reference_km':round(sd['ga_ref_km'],1) if sd['ga_ref_km'] is not None else None,
            'snap_distance_m':round(sd['snap_m'],1),
            'distance_to_next_km':sd['dist_to_next'],'next_station':sd['next_station'],
            'is_branch':sd['is_branch'],'branch_type':sd['branch_type']}})

    gj={'type':'FeatureCollection',
        'crs':{'type':'name','properties':{'name':'urn:ogc:def:crs:OGC:1.3:CRS84'}},
        'features':features}
    with open(OGJN,'w',encoding='utf-8') as f: json.dump(gj,f,indent=2,ensure_ascii=False)
    gjs=os.path.getsize(OGJN)
    rc=sum(1 for ft2 in features if ft2['properties']['type']=='route')
    stc=sum(1 for ft2 in features if ft2['properties']['type']=='station')
    print(f"  {OGJN}: {gjs/1024:.0f}KB ({rc} routes, {stc} stations)")

    with open(OCSV,'w',encoding='utf-8',newline='') as f:
        w=csv.writer(f)
        w.writerow(['station_name','station_id','line_name','distance_from_geneva_km',
                    'ga_reference_km','distance_to_next_km','next_station',
                    'snap_distance_m','snapped_lat','snapped_lon','is_branch','branch_type'])
        for sd in results:
            w.writerow([sd['name'],sd['sid'],sd['route'],round(sd['dist_km'],2),
                       round(sd['ga_ref_km'],1) if sd['ga_ref_km'] is not None else '',
                       sd['dist_to_next'] if sd['dist_to_next'] is not None else '',
                       sd['next_station'] or '',
                       round(sd['snap_m'],1),round(sd['snap_lat'],6),round(sd['snap_lon'],6),
                       sd['is_branch'],sd['branch_type'] or ''])
    csvs=os.path.getsize(OCSV)
    print(f"  {OCSV}: {csvs/1024:.1f}KB ({len(results)} rows)")

    # Summary
    print("\n"+"="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nSource: GeoPackage ({gs/1024/1024:.1f}MB), {len(sraw)} stations")
    print(f"Pipeline: {len(ft)} raw -> {len(f1)} non-siding -> {len(ib)} bbox -> {len(std_lines)} std + {len(nar_lines)} nar")
    print(f"Bridges: {bc}, Spine: {len(spine_matched)}/{len(MAINLINE_SPINE)}, Failed: {len(failed_conn)}")
    print(f"Corridor: {corridor_km:.1f}km merged geometry")
    print(f"Calibration: {len(clean_cal)} points, range {clean_cal[0][1]:.0f}-{clean_cal[-1][1]:.0f}km")
    print(f"Snap: <100m:{sum(1 for d in snaps if d<=100)}/{len(results)}, <300m:{sum(1 for d in snaps if d<=300)}/{len(results)}, <1km:{sum(1 for d in snaps if d<=1000)}/{len(results)}")
    if devs:
        ad2=[abs(d[3]) for d in devs]
        print(f"Distances: mean abs dev {sum(ad2)/len(ad2):.1f}km, Pearson r={pr:.4f}")
    print(f"\nOutputs:")
    print(f"  {OGJN} ({gjs/1024:.0f}KB)")
    print(f"  {OCSV} ({csvs/1024:.1f}KB)")
    print("\nDone.")

if __name__=='__main__': main()
