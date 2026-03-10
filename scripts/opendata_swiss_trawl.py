#!/usr/bin/env python3
"""
opendata.swiss TRAWL — Triple-filter dark data explorer

Three independent filters, applied POST-RETRIEVAL:
1. THEMATIC — keyword search across 10+ themes in FR/DE/EN
2. NAME MATCH — does metadata mention any of ~12,000 place names from TLM3D?
3. SPATIAL OVERLAP — does dataset's bounding box overlap City101 or Zurich corridors?

A dataset that hits multiple filters = high relevance signal.

Andrea Crespo — EPFL BA6 Studio Huang — City101 Sentient Cities
"""

import requests
import json
import time
import re
import os
from collections import defaultdict

# ============================================================
# CONFIGURATION
# ============================================================

BASE = "https://ckan.opendata.swiss/api/3/action/package_search"

CITY101_BBOX = [5.9530, 46.0374, 7.0434, 46.6047]
ZURICH_BBOX  = [8.2895, 47.1475, 8.9508, 47.6362]

PLACE_DICT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corridor_place_dictionary.json")
if os.path.exists(PLACE_DICT_PATH):
    with open(PLACE_DICT_PATH, 'r', encoding='utf-8') as f:
        place_dict = json.load(f)
    CITY101_NAMES = set(n.lower() for n in place_dict.get('city101_names', []) if len(n) > 3)
    ZURICH_NAMES = set(n.lower() for n in place_dict.get('zurich_names', []) if len(n) > 3)
    print(f"Loaded place dictionary: {len(CITY101_NAMES)} City101 names, {len(ZURICH_NAMES)} Zurich names")
else:
    CITY101_NAMES = set(n.lower() for n in [
        "vaud", "geneve", "geneva", "genf", "valais", "wallis", "fribourg", "freiburg",
        "lausanne", "montreux", "vevey", "nyon", "morges", "aigle", "villeneuve",
        "renens", "prilly", "pully", "lutry", "cully", "rivaz", "st-saphorin",
        "gland", "rolle", "aubonne", "allaman", "perroy", "bursinel", "bursins",
        "coppet", "founex", "celigny", "versoix", "bellevue", "pregny", "chambesy",
        "cologny", "collonge-bellerive", "hermance", "corsier", "corseaux",
        "chardonne", "jongny", "la tour-de-peilz", "clarens", "territet",
        "veytaux", "chillon", "roche", "yvorne", "ollon", "bex",
        "monthey", "st-maurice", "martigny", "sion", "sierre",
        "leman", "lavaux", "riviera", "chablais", "la cote", "arc lemanique",
        "cff", "sbb", "epfl", "unil", "cern", "palexpo",
        "chateau de chillon", "olympic", "nestle",
    ])
    ZURICH_NAMES = set(n.lower() for n in [
        "zurich", "winterthur", "uster", "dubendorf", "dietikon",
        "wadenswil", "horgen", "adliswil", "thalwil", "kilchberg",
        "ruschlikon", "rapperswil", "pfaffikon", "meilen", "stafa",
        "mannedorf", "kusnacht", "zollikon", "erlenbach", "herrliberg",
        "oberrieden", "richterswil", "lachen", "wollerau", "freienbach",
        "zurichsee", "limmat", "sihl",
    ])
    print(f"Using fallback place names: {len(CITY101_NAMES)} City101, {len(ZURICH_NAMES)} Zurich")

SEARCH_TERMS = {
    "digital": ["wifi", "wlan", "breitband", "broadband", "mobilfunk", "5g", 
                "glasfaser", "fibre optique", "internet", "telecom", "swisscom",
                "sunrise", "salt", "antenne", "funknetz"],
    "transport": ["sbb", "cff ffs", "fahrplan", "horaire transport", "train gare bahnhof",
                  "pendler", "navetteur", "mobilite", "mobilitat",
                  "velo", "bike fahrrad", "bus tram",
                  "transport public", "offentlicher verkehr", "verkehr",
                  "haltestelle", "parking parkhaus", "e-bike",
                  "publibike", "carsharing", "mobility", "schiff bateau",
                  "noctambus nachtbus", "seilbahn funiculaire"],
    "work": ["coworking", "bureau office buro", "emploi beschaftigung",
             "entreprise unternehmen", "startup", "economie wirtschaft",
             "freelance independant", "teletravail homeoffice",
             "commerce laden", "arbeit travail"],
    "temporal": ["horaire offnungszeiten", "nuit nacht night",
                 "dimanche sonntag sunday", "frequentation frequenz",
                 "pendler statistik", "heures pointe stosszeit",
                 "tagesgang", "zeitreihe"],
    "places": ["bibliotheque bibliothek", "cafe restaurant",
               "hopital spital", "ecole schule",
               "poste post", "bancomat", "kultur culture",
               "parc park", "piscine schwimmbad", "musee museum"],
    "spatial": ["commune gemeinde", "population bevolkerung",
                "densite dichte", "cadastre kataster grundbuch",
                "zone amenagement raumplanung",
                "batiment gebaude building", "hectare",
                "statpop", "statent", "statbl"],
    "infrastructure": ["eclairage beleuchtung", "electricite strom",
                       "energie energy", "ladestation charging",
                       "infrastructure", "reseau netz",
                       "wasserversorgung eau potable", "kanalisation"],
    "comfort": ["bruit larm noise", "qualite air luftqualitat",
                "temperature temperatur", "securite sicherheit",
                "vert grun grunflache", "paysage landschaft",
                "sonneneinstrahlung ensoleillement", "umwelt environnement"],
    "demographic": ["alter age", "migration", "auslander etranger",
                    "revenu einkommen", "menage haushalt",
                    "logement wohnung", "nationalite staatsangehorigkeit",
                    "pendler navetteur commuter", "erwerbstatige actifs"],
    "lateral": [
        "vaud", "geneve geneva", "leman", "lausanne",
        "tourisme tourismus", "hotel", "congres kongress",
        "international organisation", 
        "vigne vignoble weinberg", "patrimoine kulturerbe heritage",
        "lac see lake",
        "livraison lieferung", "colis paket",
        "meteo wetter",
        "dechet abfall", "recyclage",
        "permis bewilligung baubewilligung", "construction bau",
        "accident unfall", "ambulance rettung", "polizei police",
        "chien hund", "arbre baum stadtbaum",
        "marche markt wochenmarkt", "veranstaltung evenement event",
        "sport sportanlage", "friedhof cimetiere",
        "spielplatz place de jeux", "brunnen fontaine",
        "landwirtschaft agriculture", "wald foret forest",
        "gewasser cours eau",
    ],
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def bbox_overlap(bbox1, bbox2):
    return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or 
                bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])

def parse_spatial(spatial_str):
    if not spatial_str:
        return None
    try:
        geo = json.loads(spatial_str) if isinstance(spatial_str, str) else spatial_str
        if 'coordinates' in geo:
            coords = geo['coordinates']
            flat = []
            def flatten(c):
                if isinstance(c, (list, tuple)):
                    if len(c) >= 2 and all(isinstance(x, (int, float)) for x in c[:2]):
                        flat.append(c[:2])
                    else:
                        for item in c:
                            flatten(item)
            flatten(coords)
            if flat:
                lons = [p[0] for p in flat]
                lats = [p[1] for p in flat]
                return [min(lons), min(lats), max(lons), max(lats)]
        elif 'bbox' in geo:
            return geo['bbox'][:4]
    except (json.JSONDecodeError, TypeError, KeyError):
        pass
    return None

def check_name_match(text, name_set):
    text_lower = text.lower()
    matches = []
    for name in name_set:
        if len(name) > 4:
            if re.search(r'\b' + re.escape(name) + r'\b', text_lower):
                matches.append(name)
        elif name in text_lower:
            matches.append(name)
        if len(matches) >= 5:
            break
    return matches

def get_title(ds):
    title = ds.get('title', {})
    if isinstance(title, dict):
        return title.get('fr', title.get('en', title.get('de', str(title))))
    return str(title)

def get_description(ds):
    desc = ds.get('description', {})
    if isinstance(desc, dict):
        return desc.get('fr', desc.get('en', desc.get('de', '')))
    return str(desc) if desc else ''

# ============================================================
# PHASE 1: TRAWL
# ============================================================

all_datasets = {}
total_queries = sum(len(v) for v in SEARCH_TERMS.values())
done = 0

print(f"\n{'='*60}")
print(f"PHASE 1: TRAWLING opendata.swiss ({total_queries} queries)")
print(f"{'='*60}\n")

for theme, terms in SEARCH_TERMS.items():
    for term in terms:
        done += 1
        try:
            params = {'q': term, 'rows': 50, 'sort': 'score desc'}
            resp = requests.get(BASE, params=params, timeout=15)
            data = resp.json()
            
            if data['success']:
                count = data['result']['count']
                results = data['result']['results']
                new_count = 0
                
                for ds in results:
                    ds_id = ds['name']
                    is_new = ds_id not in all_datasets
                    if is_new:
                        new_count += 1
                        orgs = ds.get('organization', {})
                        org_name = orgs.get('title', 'unknown') if orgs else 'unknown'
                        keywords = []
                        for kw in ds.get('keywords', {}).values():
                            if isinstance(kw, list):
                                keywords.extend(kw)
                        formats = set()
                        for res in ds.get('resources', []):
                            fmt = res.get('format', '').upper()
                            if fmt:
                                formats.add(fmt)
                        spatial_raw = ds.get('spatial', '')
                        
                        all_datasets[ds_id] = {
                            'title': get_title(ds),
                            'description': get_description(ds)[:500],
                            'organization': org_name,
                            'keywords': keywords[:15],
                            'formats': sorted(formats),
                            'themes': set(),
                            'search_terms': set(),
                            'spatial_raw': spatial_raw,
                            'spatial_bbox': parse_spatial(spatial_raw),
                            'num_resources': len(ds.get('resources', [])),
                            'url': f"https://opendata.swiss/en/dataset/{ds_id}",
                            'overlaps_city101': False,
                            'overlaps_zurich': False,
                            'city101_name_matches': [],
                            'zurich_name_matches': [],
                        }
                    
                    all_datasets[ds_id]['themes'].add(theme)
                    all_datasets[ds_id]['search_terms'].add(term)
                
                print(f"  [{done:3d}/{total_queries}] [{theme:15s}] '{term}' -> {count:5d} total, {len(results):2d} returned, {new_count:2d} new  (cumulative: {len(all_datasets)})", flush=True)
            
            time.sleep(0.25)
            
        except Exception as e:
            print(f"  [{done:3d}/{total_queries}] [{theme:15s}] '{term}' -> ERROR: {e}", flush=True)

print(f"\n  TOTAL UNIQUE DATASETS COLLECTED: {len(all_datasets)}")

# ============================================================
# PHASE 2: GEOGRAPHIC FILTERS
# ============================================================

print(f"\n{'='*60}")
print(f"PHASE 2: APPLYING GEOGRAPHIC FILTERS")
print(f"{'='*60}\n")

bbox_hits_c101 = 0
bbox_hits_zh = 0
name_hits_c101 = 0
name_hits_zh = 0

for ds_id, info in all_datasets.items():
    bbox = info['spatial_bbox']
    if bbox:
        if bbox_overlap(bbox, CITY101_BBOX):
            info['overlaps_city101'] = True
            bbox_hits_c101 += 1
        if bbox_overlap(bbox, ZURICH_BBOX):
            info['overlaps_zurich'] = True
            bbox_hits_zh += 1
    
    searchable_text = info['title'] + ' ' + info['description'] + ' ' + ' '.join(info['keywords'])
    
    c101_matches = check_name_match(searchable_text, CITY101_NAMES)
    if c101_matches:
        info['city101_name_matches'] = c101_matches
        name_hits_c101 += 1
    
    zh_matches = check_name_match(searchable_text, ZURICH_NAMES)
    if zh_matches:
        info['zurich_name_matches'] = zh_matches
        name_hits_zh += 1

print(f"  Bounding box overlap — City101: {bbox_hits_c101}, Zurich: {bbox_hits_zh}")
print(f"  Name mentions       — City101: {name_hits_c101}, Zurich: {name_hits_zh}")

# ============================================================
# PHASE 3: ANALYSIS & OUTPUT
# ============================================================

print(f"\n{'='*60}")
print(f"PHASE 3: ANALYSIS")
print(f"{'='*60}")

def relevance_score(info):
    score = 0
    score += len(info['themes'])
    score += 3 if info['overlaps_city101'] else 0
    score += 2 if info['overlaps_zurich'] else 0
    score += 2 if info['city101_name_matches'] else 0
    score += 1 if info['zurich_name_matches'] else 0
    return score

scored = [(ds_id, info, relevance_score(info)) for ds_id, info in all_datasets.items()]
scored.sort(key=lambda x: -x[2])

print(f"\n\n## TOP 50 MOST RELEVANT DATASETS\n")
for rank, (ds_id, info, score) in enumerate(scored[:50], 1):
    themes = ', '.join(sorted(info['themes']))
    formats = ', '.join(info['formats'][:5])
    flags = []
    if info['overlaps_city101']: flags.append("BBOX-C101")
    if info['overlaps_zurich']: flags.append("BBOX-ZH")
    if info['city101_name_matches']: flags.append(f"NAMES-C101:{','.join(info['city101_name_matches'][:3])}")
    if info['zurich_name_matches']: flags.append(f"NAMES-ZH:{','.join(info['zurich_name_matches'][:3])}")
    
    print(f"#{rank:2d} [score={score}] {info['title']}")
    print(f"    org: {info['organization']}")
    print(f"    themes: {themes} | formats: {formats}")
    print(f"    flags: {' | '.join(flags) if flags else 'keyword-only'}")
    print(f"    {info['url']}")
    print()

c101_relevant = [(k, v, relevance_score(v)) for k, v in all_datasets.items() 
                 if v['overlaps_city101'] or v['city101_name_matches']]
c101_relevant.sort(key=lambda x: -x[2])

print(f"\n{'='*60}")
print(f"CITY101 CORRIDOR — {len(c101_relevant)} geographically relevant datasets")
print(f"{'='*60}\n")
for ds_id, info, score in c101_relevant[:60]:
    themes = ', '.join(sorted(info['themes']))
    formats = ', '.join(info['formats'][:4])
    flags = []
    if info['overlaps_city101']: flags.append("BBOX")
    if info['city101_name_matches']: flags.append(f"names: {', '.join(info['city101_name_matches'][:4])}")
    print(f"  [{score}] {info['title']}")
    print(f"      {info['organization']} | {formats} | {' + '.join(flags)}")
    print(f"      themes: {themes}")
    print(f"      {info['url']}")
    print()

zh_relevant = [(k, v, relevance_score(v)) for k, v in all_datasets.items()
               if v['overlaps_zurich'] or v['zurich_name_matches']]
zh_relevant.sort(key=lambda x: -x[2])

print(f"\n{'='*60}")
print(f"ZURICH — {len(zh_relevant)} geographically relevant datasets")
print(f"{'='*60}\n")
for ds_id, info, score in zh_relevant[:30]:
    print(f"  [{score}] {info['title']}")
    print(f"      {info['organization']} | {', '.join(info['formats'][:4])}")
    print(f"      {info['url']}")
    print()

multi = [(k, v) for k, v in all_datasets.items() if len(v['themes']) >= 3]
multi.sort(key=lambda x: -len(x[1]['themes']))

print(f"\n{'='*60}")
print(f"MULTI-THEME INTERSECTIONS (>=3 themes) — {len(multi)} datasets")
print(f"{'='*60}\n")
for ds_id, info in multi[:40]:
    themes = ', '.join(sorted(info['themes']))
    print(f"  [{len(info['themes'])} themes: {themes}] {info['title']}")
    print(f"      {info['organization']} | {', '.join(info['formats'][:4])}")
    print(f"      {info['url']}")
    print()

print(f"\n{'='*60}")
print(f"THEME BREAKDOWN")
print(f"{'='*60}\n")
for theme in SEARCH_TERMS:
    theme_ds = [(k, v) for k, v in all_datasets.items() if theme in v['themes']]
    unique = [(k, v) for k, v in theme_ds if len(v['themes']) == 1]
    geo = [(k, v) for k, v in theme_ds if v['overlaps_city101'] or v['city101_name_matches']]
    print(f"  {theme:15s}: {len(theme_ds):4d} total | {len(unique):4d} unique | {len(geo):4d} geo-relevant")

print(f"\n{'='*60}")
print(f"TOP DATA PUBLISHERS")
print(f"{'='*60}\n")
org_counts = defaultdict(int)
for ds in all_datasets.values():
    org_counts[ds['organization']] += 1
for org, count in sorted(org_counts.items(), key=lambda x: -x[1])[:25]:
    print(f"  {count:4d} — {org}")

print(f"\n{'='*60}")
print(f"FORMAT CENSUS")
print(f"{'='*60}\n")
fmt_counts = defaultdict(int)
for ds in all_datasets.values():
    for f in ds['formats']:
        fmt_counts[f] += 1
for fmt, count in sorted(fmt_counts.items(), key=lambda x: -x[1])[:20]:
    print(f"  {count:4d} — {fmt}")

# ---- SAVE FULL JSON ----
# Output goes to the output/ folder, not scripts/
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "opendata_trawl_full.json")

serializable = {}
for k, v in all_datasets.items():
    sv = dict(v)
    sv['themes'] = sorted(v['themes'])
    sv['search_terms'] = sorted(v['search_terms'])
    sv['relevance_score'] = relevance_score(v)
    del sv['spatial_raw']
    serializable[k] = sv

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(serializable, f, ensure_ascii=False, indent=2)
print(f"\nFull results saved to: {output_path}")

print(f"\n{'='*60}")
print(f"DONE — {len(all_datasets)} datasets catalogued")
print(f"{'='*60}")
