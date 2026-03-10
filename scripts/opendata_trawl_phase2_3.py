#!/usr/bin/env python3
"""
opendata.swiss TRAWL — Phases 2 + 3
Geographic filtering, name matching, scoring, and ranking.

Reads cached Phase 1 results from output/ and produces:
  - output/opendata_swiss_trawl_ranked.csv
  - output/opendata_swiss_trawl_top50.md

Andrea Crespo — EPFL BA6 Studio Huang — City101 Sentient Cities
"""

import json
import csv
import re
import os
import sys
from collections import defaultdict, Counter
import time

# ============================================================
# PATHS
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")

RAW_PATH = os.path.join(OUTPUT_DIR, "trawl_all_raw.json")
SPATIAL_PATH = os.path.join(OUTPUT_DIR, "trawl_spatial.json")
PLACE_DICT_PATH = os.path.join(SCRIPT_DIR, "corridor_place_dictionary.json")

CSV_OUTPUT = os.path.join(OUTPUT_DIR, "opendata_swiss_trawl_ranked.csv")
MD_OUTPUT = os.path.join(OUTPUT_DIR, "opendata_swiss_trawl_top50.md")

# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("OPENDATA.SWISS TRAWL — PHASES 2 + 3")
print("=" * 70)

print("\nLoading cached data...")

with open(RAW_PATH, 'r', encoding='utf-8') as f:
    all_raw = json.load(f)
print(f"  trawl_all_raw.json: {len(all_raw)} datasets")

with open(SPATIAL_PATH, 'r', encoding='utf-8') as f:
    spatial_data = json.load(f)
non_empty_spatial = sum(1 for v in spatial_data.values() if v)
print(f"  trawl_spatial.json: {len(spatial_data)} entries, {non_empty_spatial} with spatial data")

with open(PLACE_DICT_PATH, 'r', encoding='utf-8') as f:
    place_dict = json.load(f)
city101_names_raw = place_dict.get('city101_names', [])
print(f"  corridor_place_dictionary.json: {len(city101_names_raw)} City101 names")

# ============================================================
# HELPER: extract text from multilingual fields
# ============================================================

def extract_text(field):
    """Extract text from a field that might be a string, dict, or None."""
    if field is None:
        return ""
    if isinstance(field, str):
        return field
    if isinstance(field, dict):
        # Prefer FR, then DE, then EN, then IT, then any
        for lang in ['fr', 'de', 'en', 'it']:
            if lang in field and field[lang]:
                return str(field[lang])
        # Try any non-empty value
        for v in field.values():
            if v:
                return str(v)
    return str(field)

# ============================================================
# BUILD SEARCHABLE TEXT PER DATASET
# ============================================================

print("\nBuilding searchable text for all datasets...")

dataset_texts = {}  # slug -> lowercased combined text
dataset_info = {}   # slug -> normalized info dict

for slug, raw in all_raw.items():
    title = extract_text(raw.get('title', ''))
    description = extract_text(raw.get('description', ''))
    organization = extract_text(raw.get('organization', ''))

    # Keywords can be a list of strings or a dict of lists
    keywords_raw = raw.get('keywords', [])
    if isinstance(keywords_raw, dict):
        keywords = []
        for v in keywords_raw.values():
            if isinstance(v, list):
                keywords.extend(v)
            elif isinstance(v, str):
                keywords.append(v)
    elif isinstance(keywords_raw, list):
        keywords = keywords_raw
    else:
        keywords = []

    # Formats
    formats_raw = raw.get('formats', [])
    if isinstance(formats_raw, list):
        formats = [str(f).upper() for f in formats_raw]
    else:
        formats = []

    # Themes and search_terms — can be list or set-like
    themes = raw.get('themes', [])
    if isinstance(themes, list):
        themes = themes
    else:
        themes = list(themes) if themes else []

    search_terms = raw.get('search_terms', [])
    if isinstance(search_terms, list):
        search_terms = search_terms
    else:
        search_terms = list(search_terms) if search_terms else []

    # Build combined searchable text (lowercased)
    # NOTE: organization is included for place name matching but NOT for thematic
    # matching, because "Office fédéral..." contains "office" which false-matches
    # the coworking theme on nearly every federal dataset
    combined = ' '.join([
        title, description, organization,
        ' '.join(keywords),
        ' '.join(themes),
        ' '.join(search_terms)
    ]).lower()

    # Separate text for thematic matching (excludes organization name)
    thematic_text = ' '.join([
        title, description,
        ' '.join(keywords),
        ' '.join(themes),
        ' '.join(search_terms)
    ]).lower()

    dataset_texts[slug] = combined
    dataset_info[slug] = {
        'title': title,
        'description': description[:500],
        'organization': organization,
        'keywords': keywords,
        'formats': formats,
        'themes': themes,
        'search_terms': search_terms,
        'num_resources': raw.get('num_resources', 0),
        'url': raw.get('url', f'https://opendata.swiss/en/dataset/{slug}'),
        '_thematic_text': thematic_text,
    }

print(f"  Built searchable text for {len(dataset_texts)} datasets")

# ============================================================
# PHASE 2A: SPATIAL SCORING
# ============================================================

print("\n" + "=" * 70)
print("PHASE 2A: SPATIAL SCORING")
print("=" * 70)

# Canton / region patterns for scoring
# Use word-boundary matching to avoid substring false positives
# (e.g., "ge" matching "Ingenbohl", "vd" matching random words)

# Exact corridor cantons/cities → high
HIGH_SPATIAL_LONG = [
    'genève', 'geneve', 'geneva', 'genf',
    'vaud', 'waadt',
    'lausanne', 'nyon', 'morges', 'montreux', 'vevey', 'villeneuve',
    'aigle', 'renens', 'pully', 'lutry', 'rolle', 'gland',
    'la tour-de-peilz', 'la côte', 'riviera', 'lavaux', 'chablais',
    'arc lémanique', 'lac léman', 'léman', 'leman',
    'canton de genève', 'canton de vaud', 'kanton waadt', 'kanton genf',
    'ville de lausanne', 'ville de morges', 'ville de nyon',
]

# National coverage → medium
MEDIUM_SPATIAL = [
    'schweiz', 'suisse', 'svizzera', 'switzerland', 'swiss',
    'kantone', 'cantons',
    'gemeinden', 'communes', 'municipalities',
    'politische gemeinden',
    'sonstige raumgliederungen',
    'grossregionen',
]

# Explicit non-corridor cantons → zero
ZERO_SPATIAL_LONG = [
    'thurgau', 'basel', 'luzern', 'solothurn', 'aargau',
    'schaffhausen', 'appenzell',
    'st. gallen', 'graubünden', 'graubunden', 'glarus',
    'schwyz', 'obwalden', 'nidwalden',
    'ticino', 'tessin',
    'liechtenstein',
    'emmen', 'stadt luzern', 'stadt bern', 'stadt zug',
    'ingenbohl', 'kanton schwyz', 'kanton luzern', 'kanton bern',
    'kanton thurgau', 'kanton basel', 'kanton aargau',
    'kanton zug', 'kanton uri', 'kanton glarus',
    'canton de berne', 'canton du jura',
]
# Short canton abbreviations — only match as exact or with clear delimiters
ZERO_SPATIAL_EXACT = [
    'tg', 'bs', 'bl', 'lu', 'be', 'so', 'ag', 'sh', 'ar', 'ai',
    'sg', 'gr', 'gl', 'sz', 'ur', 'ow', 'nw', 'zg', 'ju', 'ne', 'ti',
]

# Special: Fribourg/Valais are adjacent and partially relevant → low-medium
LOWMED_SPATIAL = [
    'fribourg', 'freiburg', 'canton de fribourg',
    'valais', 'wallis',
]

# Zurich → separate tag (not zero — useful for comparison)
ZURICH_SPATIAL = [
    'zürich', 'zurich', 'kanton zürich', 'stadt zürich',
]

spatial_scores = {}
spatial_zurich_flags = {}

for slug in all_raw:
    spatial_val = spatial_data.get(slug, '')
    if not spatial_val:
        spatial_scores[slug] = None  # unknown
        spatial_zurich_flags[slug] = False
        continue

    sv = spatial_val.lower().strip()

    # Check Zurich flag
    is_zurich = any(p in sv for p in ZURICH_SPATIAL)
    spatial_zurich_flags[slug] = is_zurich

    # Check high first (long patterns only — safe for substring matching)
    score = None
    for pattern in HIGH_SPATIAL_LONG:
        if pattern in sv:
            score = 1.0
            break

    # Check zero (wrong region)
    if score is None:
        for pattern in ZERO_SPATIAL_LONG:
            if pattern in sv:
                score = 0.0
                break

    # Check zero exact matches (short abbreviations like "TG", "BS")
    if score is None:
        # Only match if the spatial value IS the abbreviation or clearly contains it
        # in a structured format like "(TG)" or "Thurgau (TG)"
        for abbr in ZERO_SPATIAL_EXACT:
            # Match: exact value, or in parentheses "(TG)", or with space delimiters
            if sv == abbr or f'({abbr})' in sv:
                score = 0.0
                break

    if score is None:
        for pattern in LOWMED_SPATIAL:
            if pattern in sv:
                score = 0.5
                break
    if score is None:
        for pattern in MEDIUM_SPATIAL:
            if pattern in sv:
                score = 0.4  # national coverage — relevant but low specificity
                break

    # If still None, it's some other spatial reference
    if score is None:
        if is_zurich:
            score = 0.3  # Zurich — not corridor but useful for comparison
        elif 'geonames' in sv or 'http' in sv:
            score = 0.3  # some spatial info but can't determine relevance
        else:
            score = 0.1  # probably another location

    spatial_scores[slug] = score

# Stats
spatial_dist = Counter()
for v in spatial_scores.values():
    if v is None:
        spatial_dist['unknown'] += 1
    elif v >= 0.9:
        spatial_dist['high (corridor)'] += 1
    elif v >= 0.5:
        spatial_dist['medium (national/adjacent)'] += 1
    elif v > 0:
        spatial_dist['low (other)'] += 1
    else:
        spatial_dist['zero (wrong region)'] += 1

print("\nSpatial score distribution:")
for label, count in sorted(spatial_dist.items(), key=lambda x: -x[1]):
    print(f"  {count:5d} — {label}")

# ============================================================
# PHASE 2B: NAME MATCHING
# ============================================================

print("\n" + "=" * 70)
print("PHASE 2B: NAME MATCHING (11,875 place names + thematic keywords)")
print("=" * 70)

# Prepare City101 place names — filter to >3 chars and remove false positives
# These are real OSM place names that are also extremely common French/German words
NAME_STOPLIST = {
    # Common French words that are also OSM place names
    'ville', 'plan', 'place', 'la ville', 'le plan', 'les plans',
    'cartes', 'les cartes', 'la commune', 'le port', 'gare',
    'fontaine', 'en fontaine', 'marché', 'hôpitaux', 'court',
    'centre', 'forêt', 'le si', 'la clie', 'les communes',
    'les fontaines', 'la source', 'les routes', 'les branches',
    'la couve', 'les rouges', 'es pra', 'le pré', 'le milieu',
    'la scie', 'le cha', 'sur le cha', 'la cha', 'le carré',
    'le contour', 'pont', 'jura',
    'bois', 'la forêt', 'le bois', 'les bois', 'champ', 'le champ',
    'rue', 'la rue', 'les prés', 'pré', 'mont', 'le mont',
    'la côte', 'côte', 'pierre', 'la pierre', 'lac', 'le lac',
    'valais',
    # Additional false positives found in run 2
    'rente', 'musée', 'le parc', 'douane', 'courbes', 'la courbe',
    'la taille', 'la fin', 'prairie', 'le taux', 'les places',
    'en pro', 'savoie', 'communaux', 'la branche', 'le fruit',
    'les bas', 'les mises', 'le pas', 'tiers', 'en prin',
    'tour', 'la tour', 'la cour', 'la sau', 'le tour',
    'les vignes', 'vignes',
    # Common geographic/administrative words
    'canton', 'commune', 'district', 'région', 'zone',
    'route', 'chemin', 'passage', 'terrain', 'secteur',
    'quartier', 'lotissement', 'parcelle',
    # Common German words that are place names
    'stein', 'berg', 'wald', 'feld', 'dorf', 'bach',
    'graben', 'rain', 'bühl', 'matt', 'weid',
}

city101_names = set()
for name in city101_names_raw:
    n = name.strip().lower()
    if len(n) > 3 and n not in NAME_STOPLIST:
        city101_names.add(n)
print(f"  City101 place names (>3 chars, stoplist filtered): {len(city101_names)}")

# Zurich comparison names (from script fallback since dict has 0)
ZURICH_NAMES = set(n.lower() for n in [
    "zürich", "zurich", "winterthur", "uster", "dübendorf", "dubendorf",
    "dietikon", "wädenswil", "wadenswil", "horgen", "adliswil",
    "thalwil", "kilchberg", "rüschlikon", "ruschlikon",
    "rapperswil", "pfäffikon", "pfaffikon", "meilen", "stäfa", "stafa",
    "männedorf", "mannedorf", "küsnacht", "kusnacht", "zollikon",
    "erlenbach", "herrliberg", "oberrieden", "richterswil",
    "lachen", "wollerau", "freienbach",
    "zürichsee", "zurichsee", "limmat", "sihl",
    "s-bahn", "zvv", "vbz",
])
print(f"  Zurich comparison names: {len(ZURICH_NAMES)}")

# Thematic keywords (bilingual)
THEMATIC_KEYWORDS = {
    'transport': ['transport', 'mobilité', 'mobilite', 'mobilität', 'mobilitaet',
                  'vélo', 'velo', 'fahrrad', 'bike', 'bicycle',
                  'piéton', 'pieton', 'pedestrian', 'fussgänger', 'fussgaenger',
                  'bus', 'tram', 'metro', 'train', 'gare', 'bahnhof', 'station',
                  'sbb', 'cff', 'pendler', 'navetteur', 'commuter'],
    'energy': ['énergie', 'energie', 'energy', 'charging', 'recharge',
               'ladestation', 'borne', 'elektro', 'strom', 'electricity',
               'solaire', 'solar', 'photovoltaik'],
    'digital': ['wifi', 'wlan', 'connectivity', 'télécommunication', 'telecommunication',
                'telekommunikation', 'breitband', 'broadband', 'fibre', 'glasfaser',
                '5g', '4g', 'mobilfunk', 'internet', 'digital'],
    'noise_environment': ['bruit', 'lärm', 'laerm', 'noise',
                          'qualité de l\'air', 'luftqualität', 'luftqualitaet', 'air quality',
                          'environnement', 'umwelt', 'environment',
                          'climat', 'klima', 'climate',
                          'température', 'temperatur', 'temperature'],
    'tourism_heritage': ['tourisme', 'tourismus', 'tourism',
                         'patrimoine', 'kulturerbe', 'heritage',
                         'monument', 'musée', 'museum',
                         'lac', 'see', 'lake'],
    'urban_planning': ['urbanisme', 'stadtplanung', 'urban planning',
                       'logement', 'wohnung', 'housing',
                       'construction', 'bau', 'building',
                       'zone', 'aménagement', 'amenagement', 'raumplanung',
                       'cadastre', 'kataster', 'grundbuch'],
    'population': ['population', 'bevölkerung', 'bevoelkerung',
                   'emploi', 'beschäftigung', 'beschaeftigung', 'employment',
                   'travail', 'arbeit', 'work',
                   'commerce', 'handel', 'trade',
                   'démographie', 'demographie', 'demography'],
    'public_space': ['espace public', 'öffentlicher raum', 'oeffentlicher raum', 'public space',
                     'parc', 'park', 'jardin', 'garten', 'garden',
                     'fontaine', 'brunnen', 'fountain',
                     'place', 'platz', 'square',
                     'marché', 'markt', 'market'],
    'coworking': ['coworking', 'co-working', 'bureau', 'büro', 'buero', 'office',
                  'bibliothèque', 'bibliotheque', 'bibliothek', 'library',
                  'café', 'cafe', 'restaurant'],
    'safety': ['sécurité', 'securite', 'sicherheit', 'safety',
               'accident', 'unfall', 'police', 'polizei',
               'éclairage', 'eclairage', 'beleuchtung', 'lighting'],
}

# Flatten thematic keywords for matching, and track which theme each belongs to
thematic_term_to_theme = {}
all_thematic_terms = set()
for theme, terms in THEMATIC_KEYWORDS.items():
    for term in terms:
        t = term.lower()
        all_thematic_terms.add(t)
        thematic_term_to_theme[t] = theme

print(f"  Thematic keywords: {len(all_thematic_terms)} across {len(THEMATIC_KEYWORDS)} themes")

# ---- THE BIG MATCH ----
# For each dataset, find which place names and thematic keywords appear

print(f"\nRunning name + thematic matching across {len(dataset_texts)} datasets...")
t0 = time.time()

# Pre-sort place names by length (longer = more specific = check first)
# Also split into "word-boundary safe" (>4 chars) and "substring" (<=4 chars)
place_names_long = sorted([n for n in city101_names if len(n) > 4], key=len, reverse=True)
place_names_short = sorted([n for n in city101_names if len(n) <= 4], key=len, reverse=True)

# Results storage
name_matches = {}      # slug -> list of matched City101 place names
zurich_matches = {}    # slug -> list of matched Zurich names
thematic_matches = {}  # slug -> dict of theme -> list of matched terms

progress_interval = 500
processed = 0

for slug, text in dataset_texts.items():
    # --- City101 place name matching ---
    matched_places = []

    # Long names: use word boundary regex for precision
    for name in place_names_long:
        # Use word boundary for names > 4 chars
        if name in text:
            # Verify it's a word boundary match (not substring of larger word)
            # For names with spaces/hyphens, simple 'in' is fine
            if ' ' in name or '-' in name:
                matched_places.append(name)
            else:
                # Check word boundary
                pattern = r'\b' + re.escape(name) + r'\b'
                if re.search(pattern, text):
                    matched_places.append(name)

    # Short names (<=4 chars): require word boundary match to avoid false positives
    for name in place_names_short:
        pattern = r'\b' + re.escape(name) + r'\b'
        if re.search(pattern, text):
            matched_places.append(name)

    name_matches[slug] = matched_places

    # --- Zurich name matching ---
    matched_zh = []
    for name in ZURICH_NAMES:
        if len(name) > 4:
            if name in text:
                if ' ' in name or '-' in name:
                    matched_zh.append(name)
                else:
                    if re.search(r'\b' + re.escape(name) + r'\b', text):
                        matched_zh.append(name)
        else:
            if re.search(r'\b' + re.escape(name) + r'\b', text):
                matched_zh.append(name)
    zurich_matches[slug] = matched_zh

    # --- Thematic keyword matching (uses thematic_text, excludes org name) ---
    thematic_text = dataset_info[slug]['_thematic_text']
    matched_themes = defaultdict(list)
    for term in all_thematic_terms:
        if len(term) > 4:
            if term in thematic_text:
                theme = thematic_term_to_theme[term]
                matched_themes[theme].append(term)
        else:
            if re.search(r'\b' + re.escape(term) + r'\b', thematic_text):
                theme = thematic_term_to_theme[term]
                matched_themes[theme].append(term)
    thematic_matches[slug] = dict(matched_themes)

    processed += 1
    if processed % progress_interval == 0:
        elapsed = time.time() - t0
        print(f"  {processed}/{len(dataset_texts)} datasets processed ({elapsed:.1f}s)")

elapsed = time.time() - t0
print(f"  DONE: {processed} datasets processed in {elapsed:.1f}s")

# Stats
datasets_with_places = sum(1 for v in name_matches.values() if v)
datasets_with_zurich = sum(1 for v in zurich_matches.values() if v)
datasets_with_themes = sum(1 for v in thematic_matches.values() if v)
total_place_hits = sum(len(v) for v in name_matches.values())

print(f"\n  Datasets with City101 place name matches: {datasets_with_places}")
print(f"  Datasets with Zurich name matches: {datasets_with_zurich}")
print(f"  Datasets with thematic keyword matches: {datasets_with_themes}")
print(f"  Total individual place name hits: {total_place_hits}")

# Top matched place names
place_hit_counts = Counter()
for matches in name_matches.values():
    for m in matches:
        place_hit_counts[m] += 1
print(f"\n  Most frequently matched place names:")
for name, count in place_hit_counts.most_common(25):
    print(f"    {count:4d} — {name}")

# ============================================================
# PHASE 3: SCORING + RANKING
# ============================================================

print("\n" + "=" * 70)
print("PHASE 3: SCORING + RANKING")
print("=" * 70)

# Scoring weights:
#   Spatial match:     30%
#   Name match count:  30%
#   Thematic match:    25%
#   Data usability:    15%

# Non-corridor cantons mentioned in titles → apply penalty
NON_CORRIDOR_TITLE_PATTERNS = [
    'bâle', 'basel', 'bale',
    'argovie', 'aargau',
    'thurgovie', 'thurgau', 'turgovie',
    'uri', 'glaris', 'glarus',
    'nidwald', 'nidwalden', 'obwald', 'obwalden',
    'schwytz', 'schwyz', 'schaffhouse', 'schaffhausen',
    'soleure', 'solothurn',
    'appenzell', 'grisons', 'graubünden',
    'tessin', 'ticino', 'lucerne', 'luzern',
    'zoug', 'zug', 'st-gall', 'st. gallen',
]

# Usability scoring for formats
HIGH_USABILITY = {'CSV', 'GEOJSON', 'GPKG', 'GEOPACKAGE', 'WMS', 'WFS', 'WCS',
                  'SHAPEFILE', 'SHP', 'KML', 'KMZ', 'PARQUET', 'JSON', 'XLSX',
                  'XLS', 'SPARQL', 'GPX', 'GDB', 'SQLITE', 'TIFF', 'GEOTIFF'}
MED_USABILITY = {'XML', 'RDF', 'N3', 'RDF TURTLE', 'RDF XML', 'JSON-LD',
                 'ZIP', 'OCTET', 'TXT', 'TSV', 'ODS'}
LOW_USABILITY = {'PDF', 'HTML', 'DOC', 'DOCX', 'PNG', 'JPG', 'JPEG', 'SVG'}

# Compute max values for normalization
max_name_count = max((len(v) for v in name_matches.values()), default=1)
max_theme_count = max((sum(len(terms) for terms in v.values()) for v in thematic_matches.values()), default=1)

print(f"\n  Max place name matches in a single dataset: {max_name_count}")
print(f"  Max thematic keyword matches in a single dataset: {max_theme_count}")

# Score each dataset
results = []

for slug in all_raw:
    info = dataset_info[slug]

    # --- Spatial score (0-100, weight 30%) ---
    sp = spatial_scores.get(slug)
    if sp is not None:
        spatial_score = sp * 100
    else:
        # No spatial data → 30 (neutral — don't penalize, don't reward)
        spatial_score = 30.0

    # Title-based penalty: if the title explicitly names a non-corridor canton,
    # reduce spatial score (even if spatial metadata says "Schweiz")
    title_lower = info['title'].lower()
    for pattern in NON_CORRIDOR_TITLE_PATTERNS:
        if pattern in title_lower:
            spatial_score = min(spatial_score, 10.0)
            break

    # --- Name match score (0-100, weight 30%) ---
    nm = name_matches.get(slug, [])
    if nm:
        # Use log-ish scaling: 1 match = decent, 5+ = great, 20+ = max
        raw_nm = min(len(nm), 30)
        name_score = min(100, (raw_nm / 10) * 100)
    else:
        name_score = 0.0

    # --- Thematic score (0-100, weight 25%) ---
    tm = thematic_matches.get(slug, {})
    if tm:
        # Count unique themes hit + total term matches
        themes_hit = len(tm)
        terms_hit = sum(len(v) for v in tm.values())
        # Multi-theme bonus: hitting 3+ themes is very relevant
        theme_score = min(100, (themes_hit / 4) * 50 + (terms_hit / 8) * 50)
    else:
        theme_score = 0.0

    # --- Usability score (0-100, weight 15%) ---
    fmts = set(info['formats'])
    if fmts & HIGH_USABILITY:
        usability_score = 100.0
    elif fmts & MED_USABILITY:
        usability_score = 60.0
    elif fmts & LOW_USABILITY:
        usability_score = 30.0
    elif fmts:
        usability_score = 20.0
    else:
        usability_score = 0.0

    # --- Composite score ---
    relevance = (
        spatial_score * 0.30 +
        name_score * 0.30 +
        theme_score * 0.25 +
        usability_score * 0.15
    )

    # Zurich relevance
    zh = zurich_matches.get(slug, [])
    zurich_relevant = len(zh) > 0

    # Collect matched themes as flat list
    matched_theme_names = sorted(tm.keys()) if tm else []
    matched_theme_terms = []
    for theme_terms in tm.values():
        matched_theme_terms.extend(theme_terms)

    results.append({
        'slug': slug,
        'title': info['title'],
        'url': info['url'],
        'organization': info['organization'],
        'relevance_score': round(relevance, 2),
        'spatial_score': round(spatial_score, 2),
        'name_match_score': round(name_score, 2),
        'thematic_score': round(theme_score, 2),
        'usability_score': round(usability_score, 2),
        'matched_places': ', '.join(sorted(set(nm))[:20]),
        'matched_places_count': len(nm),
        'matched_themes': ', '.join(matched_theme_names),
        'matched_theme_terms': ', '.join(sorted(set(matched_theme_terms))[:15]),
        'formats': ', '.join(sorted(fmts)),
        'zurich_relevant': zurich_relevant,
        'zurich_names': ', '.join(sorted(set(zh))),
        'description': info['description'][:200].replace('\n', ' ').replace('\r', ' '),
        'num_resources': info['num_resources'],
    })

# Sort by relevance score descending
results.sort(key=lambda x: -x['relevance_score'])

# Add rank
for i, r in enumerate(results, 1):
    r['rank'] = i

# ============================================================
# OUTPUT: CSV
# ============================================================

print(f"\nWriting ranked CSV to {CSV_OUTPUT}...")

csv_columns = [
    'rank', 'title', 'url', 'organization', 'relevance_score',
    'spatial_score', 'name_match_score', 'thematic_score', 'usability_score',
    'matched_places', 'matched_themes', 'formats', 'zurich_relevant',
    'description'
]

with open(CSV_OUTPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns, extrasaction='ignore')
    writer.writeheader()
    for r in results:
        writer.writerow(r)

print(f"  Written {len(results)} rows")

# ============================================================
# OUTPUT: MARKDOWN TOP 50
# ============================================================

print(f"Writing top 50 markdown to {MD_OUTPUT}...")

with open(MD_OUTPUT, 'w', encoding='utf-8') as f:
    f.write("# opendata.swiss Trawl — Top 50 Most Relevant Datasets\n\n")
    f.write(f"**City101 corridor (Geneva → Villeneuve)**\n\n")
    f.write(f"Scored on: spatial overlap (30%), place name matches (30%), ")
    f.write(f"thematic relevance (25%), data usability (15%)\n\n")
    f.write(f"Total datasets scanned: {len(results)}\n\n")
    f.write("---\n\n")

    for r in results[:50]:
        f.write(f"### #{r['rank']}. {r['title']}\n\n")
        f.write(f"**Score: {r['relevance_score']}** | ")
        f.write(f"Spatial: {r['spatial_score']} | Names: {r['name_match_score']} | ")
        f.write(f"Thematic: {r['thematic_score']} | Usability: {r['usability_score']}\n\n")
        f.write(f"- **Organization:** {r['organization']}\n")
        f.write(f"- **Formats:** {r['formats']}\n")
        if r['matched_places']:
            f.write(f"- **Matched places:** {r['matched_places']}\n")
        if r['matched_themes']:
            f.write(f"- **Matched themes:** {r['matched_themes']}\n")
        if r['zurich_relevant']:
            f.write(f"- **Also covers Zurich:** Yes ({r['zurich_names']})\n")
        if r['description']:
            f.write(f"- **Description:** {r['description']}\n")
        f.write(f"- **Link:** [{r['url']}]({r['url']})\n")
        f.write(f"\n---\n\n")

print(f"  Written top 50 entries")

# ============================================================
# TERMINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

scored_above_0 = sum(1 for r in results if r['relevance_score'] > 0)
scored_above_20 = sum(1 for r in results if r['relevance_score'] > 20)
scored_above_40 = sum(1 for r in results if r['relevance_score'] > 40)
scored_above_60 = sum(1 for r in results if r['relevance_score'] > 60)
zurich_count = sum(1 for r in results if r['zurich_relevant'])

print(f"\n  Total datasets scanned:    {len(results)}")
print(f"  Scored > 0:                {scored_above_0}")
print(f"  Scored > 20:               {scored_above_20}")
print(f"  Scored > 40:               {scored_above_40}")
print(f"  Scored > 60:               {scored_above_60}")
print(f"  Zurich-relevant:           {zurich_count}")

print(f"\n\n{'─' * 70}")
print("TOP 30 DATASETS BY RELEVANCE SCORE")
print(f"{'─' * 70}\n")

for r in results[:30]:
    zh_flag = " [ZH]" if r['zurich_relevant'] else ""
    places_preview = r['matched_places'][:60] + "..." if len(r['matched_places']) > 60 else r['matched_places']
    print(f"  #{r['rank']:2d}  [{r['relevance_score']:5.1f}]  {r['title'][:65]}{zh_flag}")
    print(f"        org: {r['organization'][:50]}")
    print(f"        spatial={r['spatial_score']:.0f} names={r['name_match_score']:.0f} themes={r['thematic_score']:.0f} usability={r['usability_score']:.0f}")
    if places_preview:
        print(f"        places: {places_preview}")
    if r['matched_themes']:
        print(f"        themes: {r['matched_themes']}")
    print()

# Theme breakdown
print(f"\n{'─' * 70}")
print("THEME BREAKDOWN")
print(f"{'─' * 70}\n")

theme_counts = Counter()
for r in results:
    if r['matched_themes']:
        for t in r['matched_themes'].split(', '):
            theme_counts[t] += 1

for theme, count in theme_counts.most_common():
    # Count how many of these are in top 100
    top100_count = sum(1 for r in results[:100] if theme in r['matched_themes'])
    print(f"  {theme:25s}: {count:5d} total | {top100_count:3d} in top 100")

# Score distribution
print(f"\n{'─' * 70}")
print("SCORE DISTRIBUTION")
print(f"{'─' * 70}\n")

brackets = [(80, 100), (60, 80), (40, 60), (20, 40), (1, 20), (0, 1)]
for lo, hi in brackets:
    count = sum(1 for r in results if lo <= r['relevance_score'] < hi)
    print(f"  {lo:3d}–{hi:3d}: {count:5d} datasets")

# Format census
print(f"\n{'─' * 70}")
print("FORMAT CENSUS (all datasets)")
print(f"{'─' * 70}\n")

fmt_counts = Counter()
for r in results:
    for fmt in r['formats'].split(', '):
        if fmt.strip():
            fmt_counts[fmt.strip()] += 1
for fmt, count in fmt_counts.most_common(20):
    print(f"  {count:5d} — {fmt}")

# Top publishers
print(f"\n{'─' * 70}")
print("TOP PUBLISHERS (datasets in top 200)")
print(f"{'─' * 70}\n")

pub_counts = Counter()
for r in results[:200]:
    pub_counts[r['organization']] += 1
for org, count in pub_counts.most_common(15):
    print(f"  {count:4d} — {org[:70]}")

print(f"\n{'=' * 70}")
print(f"OUTPUT FILES:")
print(f"  {CSV_OUTPUT}")
print(f"  {MD_OUTPUT}")
print(f"{'=' * 70}")
print("DONE.")
