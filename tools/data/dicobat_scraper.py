#!/usr/bin/env python3
"""
Dicobat Online Scraper
======================
Extracts the full Dicobat construction dictionary into structured markdown files.

Two stages:
  1. Discovery (no auth): crawl themes → subcategories → term URLs → url_inventory.json
  2. Extraction (needs auth cookies): fetch each term page → structured markdown

Usage:
  # Discovery only (no cookies needed)
  python tools/data/dicobat_scraper.py discover

  # Extract all terms (needs cookies)
  python tools/data/dicobat_scraper.py extract

  # Extract a single subcategory (for testing)
  python tools/data/dicobat_scraper.py extract --subcategory 50100

  # Resume interrupted extraction
  python tools/data/dicobat_scraper.py extract --resume

Cookie setup:
  Create output/dicobat/.cookies.json:
  {
    "PHPSESSID": "your_session_id_here"
  }
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)


# --- Configuration ---

BASE_URL = "https://www.dicobatonline.fr"
# Knowledge lives in standalone archibase repo — override with ARCHIBASE_PATH env var
KNOWLEDGE_ROOT = Path(os.environ.get("ARCHIBASE_PATH", Path.home() / "CLAUDE" / "archibase"))
PROJECT_ROOT = KNOWLEDGE_ROOT if KNOWLEDGE_ROOT.exists() else Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "output" / "dicobat"
SOURCE_DIR = PROJECT_ROOT / "source" / "dicobat"
COOKIES_FILE = OUTPUT_DIR / ".cookies.json"
INVENTORY_FILE = OUTPUT_DIR / "url_inventory.json"
LOG_FILE = OUTPUT_DIR / "scrape_log.json"

# Known theme IDs and slugs (discovered from site navigation)
THEMES = [
    (1, "Architecture"),
    (2, "Description-des-batiments"),
    (3, "Materiaux-composants"),
    (4, "Proprietes-physiques"),
    (5, "Sols-infrastructures"),
    (6, "Maconnerie"),
    (7, "Charpente"),
    (8, "Couverture-etancheite"),
    (9, "Fumisterie"),
    (10, "Menuiserie"),
    (12, "Revetements-interieurs"),
    (13, "Genie-thermique"),
    (14, "Plomberie-reseaux"),
    (16, "Electricite-eclairage"),
    (17, "Serrurerie-ferronnerie"),
    (18, "Securite"),
    (19, "Outils-materiel-quincaillerie"),
    (20, "Fixations-collages-joints"),
    (110000, "Vitrerie-miroiterie"),
    (150000, "Acoustique"),
    (200304, "Metiers"),
]

REQUEST_DELAY = 1.5  # seconds between requests (respectful rate limiting)

# --- Session setup ---


def make_session(cookies_required=False):
    """Create a requests session, optionally with auth cookies.

    When cookies are provided, visits the homepage first to establish
    the full server-side session (the site sets additional cookies and
    session state on first page load).
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    })

    if cookies_required:
        if not COOKIES_FILE.exists():
            print(f"ERROR: Cookie file not found at {COOKIES_FILE}")
            print("Create it with your session cookies:")
            print('  {"PHPSESSID": "your_session_id"}')
            sys.exit(1)

        with open(COOKIES_FILE) as f:
            cookies = json.load(f)

        for name, value in cookies.items():
            session.cookies.set(name, value, domain="www.dicobatonline.fr")

        print(f"Loaded {len(cookies)} cookie(s) from {COOKIES_FILE}")

        # Visit homepage to establish full session — the server sets
        # additional cookies (cookie_login, cookie_mdp) on first load
        # and term pages return empty content without this step.
        print("Establishing session (visiting homepage)...")
        session.get(f"{BASE_URL}/", timeout=30)
        print(f"Session established. Cookies: {list(session.cookies.keys())}")

    return session


def fetch_page(session, url, delay=True):
    """Fetch a page with rate limiting and error handling."""
    if delay:
        time.sleep(REQUEST_DELAY)

    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        # Server declares UTF-8 in <meta charset> but HTTP header may
        # say iso-8859-1, causing requests to double-encode accents.
        resp.encoding = "utf-8"
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


# --- Discovery ---


def discover_subcategories(session, theme_id, theme_slug):
    """Crawl a theme page to find all subcategory links."""
    url = f"{BASE_URL}/theme/{theme_id}/{theme_slug}"
    soup = fetch_page(session, url)
    if not soup:
        return []

    subcategories = []
    # Find all links matching /theme/{5-digit-code}/{slug}
    for link in soup.find_all("a", href=True):
        href = link["href"]
        match = re.match(r"/theme/(\d{4,6})/(.+)", href)
        if match:
            sub_id = int(match.group(1))
            sub_slug = match.group(2)
            # Skip if it's the theme itself
            if sub_id != theme_id:
                name = link.get_text(strip=True)
                subcategories.append({
                    "id": sub_id,
                    "slug": sub_slug,
                    "name": name,
                    "url": urljoin(BASE_URL, href),
                    "theme_id": theme_id,
                    "theme_slug": theme_slug,
                })

    # Deduplicate by id
    seen = set()
    unique = []
    for sc in subcategories:
        if sc["id"] not in seen:
            seen.add(sc["id"])
            unique.append(sc)

    return unique


def discover_terms(session, subcategory):
    """Crawl a subcategory page to find all term links."""
    soup = fetch_page(session, subcategory["url"])
    if not soup:
        return []

    terms = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        match = re.match(r"/terme/(\d+)/(.+?)(?:#.*)?$", href)
        if match:
            term_id = int(match.group(1))
            term_slug = match.group(2)
            name = link.get_text(strip=True)
            terms.append({
                "id": term_id,
                "slug": term_slug,
                "name": name,
                "url": f"{BASE_URL}/terme/{term_id}/{term_slug}",
                "subcategory_id": subcategory["id"],
                "subcategory_name": subcategory["name"],
                "theme_id": subcategory["theme_id"],
                "theme_slug": subcategory["theme_slug"],
            })

    # Deduplicate by id
    seen = set()
    unique = []
    for t in terms:
        if t["id"] not in seen:
            seen.add(t["id"])
            unique.append(t)

    return unique


def run_discovery(session):
    """Full discovery: themes → subcategories → terms."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    inventory = {
        "themes": [],
        "subcategories": [],
        "terms": [],
        "stats": {},
    }

    print(f"\n{'='*60}")
    print("DICOBAT DISCOVERY")
    print(f"{'='*60}\n")

    # Step 1: Discover subcategories for each theme
    all_subcategories = []
    for theme_id, theme_slug in THEMES:
        print(f"Theme {theme_id}: {theme_slug}")
        subcats = discover_subcategories(session, theme_id, theme_slug)
        print(f"  → {len(subcats)} subcategories")
        all_subcategories.extend(subcats)
        inventory["themes"].append({
            "id": theme_id,
            "slug": theme_slug,
            "subcategory_count": len(subcats),
        })

    inventory["subcategories"] = all_subcategories
    print(f"\nTotal subcategories: {len(all_subcategories)}")

    # Step 2: Discover terms for each subcategory
    all_terms = []
    for i, subcat in enumerate(all_subcategories):
        print(f"  [{i+1}/{len(all_subcategories)}] {subcat['name']}", end="", flush=True)
        terms = discover_terms(session, subcat)
        print(f" → {len(terms)} terms")
        all_terms.extend(terms)

    # Global deduplication (terms can appear in multiple subcategories)
    seen_ids = set()
    unique_terms = []
    for t in all_terms:
        if t["id"] not in seen_ids:
            seen_ids.add(t["id"])
            unique_terms.append(t)

    inventory["terms"] = unique_terms
    inventory["stats"] = {
        "theme_count": len(THEMES),
        "subcategory_count": len(all_subcategories),
        "total_term_refs": len(all_terms),
        "unique_terms": len(unique_terms),
        "discovery_date": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Save inventory
    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("DISCOVERY COMPLETE")
    print(f"{'='*60}")
    print(f"Themes:        {len(THEMES)}")
    print(f"Subcategories: {len(all_subcategories)}")
    print(f"Term refs:     {len(all_terms)} (with duplicates across subcats)")
    print(f"Unique terms:  {len(unique_terms)}")
    print(f"Inventory:     {INVENTORY_FILE}")
    print()

    return inventory


# --- Extraction ---


def parse_term_page(soup, term_info):
    """Parse a Dicobat term definition page into structured markdown.

    Real HTML structure (inside #gauche):
      <div id="definition">
        <h1 class="def">term name</h1>
        <span class="genre"><strong>n.m.</strong></span>
        <div>
          <h3>Définition 1</h3>
          <p>...definition text with <a href="/terme/...">cross-refs</a>...</p>
          <div class="traduction">
            <table><tr><th>FR</th><td>french</td><th>ENG</th><td>english</td></tr></table>
          </div>
          <div class="themes_assoc">
            <h4>Thème(s) associé(s) :</h4>
            <div>• <a href="/theme/...">Theme</a> > <a href="/theme/...">Sub</a></div>
          </div>
          ...more <h3>, <p>, <div class="traduction"> blocks...
        </div>
      </div>
    """
    lines = []

    # Find the definition container
    definition_div = soup.find("div", id="definition")
    if not definition_div:
        # Fallback — try #gauche
        definition_div = soup.find("div", id="gauche")

    # --- Header ---
    # Use the page's own title if available
    h1 = definition_div.find("h1", class_="def") if definition_div else None
    term_name = h1.get_text(strip=True) if h1 else term_info["name"]

    lines.append(f"# {term_name}")
    lines.append("")

    # Metadata block
    lines.append("---")
    lines.append(f"id: {term_info['id']}")
    lines.append(f"theme: {term_info['theme_slug']}")
    lines.append(f"subcategory: {term_info['subcategory_name']}")
    lines.append(f"source: {term_info['url']}")
    lines.append(f"extracted: {time.strftime('%Y-%m-%d')}")
    lines.append("---")
    lines.append("")

    if not definition_div:
        lines.append("*No content extracted — page may require authentication.*")
        return "\n".join(lines)

    # --- Genre (part of speech) ---
    genre = definition_div.find("span", class_="genre")
    if genre:
        genre_text = genre.get_text(strip=True)
        if genre_text:
            lines.append(f"*{genre_text}*")
            lines.append("")

    # --- Walk through the content div ---
    # The main content is in the <div> child of #definition (after h1 and span.genre)
    content_div = definition_div.find("div", recursive=False)
    if not content_div:
        content_div = definition_div

    all_translations = []
    all_cross_refs = []
    classification = []

    # Process children sequentially to preserve document order
    for child in content_div.children:
        if not hasattr(child, "name") or child.name is None:
            continue

        # Section headings (Définition 1, Définition 2, etc.)
        if child.name == "h3":
            heading_text = child.get_text(strip=True)
            lines.append(f"## {heading_text}")
            lines.append("")

        # Paragraphs — main definition text
        elif child.name == "p":
            text = _process_paragraph(child)
            if text:
                lines.append(text)
                lines.append("")

        # Translation tables
        elif child.name == "div" and "traduction" in (child.get("class") or []):
            translations = _extract_translations(child)
            if translations:
                all_translations.extend(translations)
                # Also inline them right where they appear
                for t in translations:
                    parts = []
                    if t.get("fr"):
                        parts.append(f"FR: {t['fr']}")
                    if t.get("en"):
                        parts.append(f"EN: {t['en']}")
                    if t.get("na"):
                        parts.append(f"NA: {t['na']}")
                    lines.append(f"> {' / '.join(parts)}")
                lines.append("")

        # Theme associations
        elif child.name == "div" and "themes_assoc" in (child.get("class") or []):
            for theme_div in child.find_all("div"):
                crumbs = [a.get_text(strip=True) for a in theme_div.find_all("a")]
                if crumbs:
                    classification.append(" > ".join(crumbs))

        # Anchor tags (section markers) — skip
        elif child.name == "a" and child.get("class") and "anchor" in child.get("class", []):
            continue

        # Nested sub-definitions or other divs
        elif child.name == "div":
            # Could be a nested content block — extract text
            text = child.get_text(strip=True)
            if text and len(text) > 20:
                lines.append(text)
                lines.append("")

    # --- Collected translations (summary at end) ---
    if all_translations:
        lines.append("## Translations")
        lines.append("")
        seen = set()
        for t in all_translations:
            key = (t.get("fr", ""), t.get("en", ""))
            if key in seen:
                continue
            seen.add(key)
            parts = []
            if t.get("fr"):
                parts.append(f"FR: {t['fr']}")
            if t.get("en"):
                parts.append(f"EN: {t['en']}")
            if t.get("na"):
                parts.append(f"NA: {t['na']}")
            lines.append(f"- {' / '.join(parts)}")
        lines.append("")

    # --- Cross-references (from inline links in paragraphs) ---
    # Collect all /terme/ links from the definition area only
    if definition_div:
        for link in definition_div.find_all("a", href=re.compile(r"/terme/\d+")):
            ref_name = link.get_text(strip=True)
            ref_href = link["href"]
            if ref_name and ref_name.lower() != term_name.lower():
                entry = f"- [{ref_name}]({ref_href})"
                if entry not in all_cross_refs:
                    all_cross_refs.append(entry)

    if all_cross_refs:
        lines.append("## Related Terms")
        lines.append("")
        lines.extend(sorted(set(all_cross_refs)))
        lines.append("")

    # --- Classification ---
    if classification:
        lines.append("## Classification")
        lines.append("")
        for c in classification:
            lines.append(f"- {c}")
        lines.append("")

    return "\n".join(lines)


def _process_paragraph(p_tag):
    """Convert a <p> tag to markdown, preserving bold/italic and inline links."""
    parts = []
    for child in p_tag.children:
        if isinstance(child, str):
            parts.append(child)
        elif child.name == "b" or child.name == "strong":
            inner = child.get_text()
            parts.append(f"**{inner}**")
        elif child.name == "i" or child.name == "em":
            inner = child.get_text()
            parts.append(f"*{inner}*")
        elif child.name == "a" and child.get("href", "").startswith("/terme/"):
            link_text = child.get_text()
            parts.append(f"[{link_text}]({child['href']})")
        elif child.name == "a" and "lightbox" in " ".join(child.get("class", [])):
            # Image reference — note it but skip the img tag
            parts.append("[illustration]")
        elif child.name == "br":
            parts.append("\n")
        else:
            parts.append(child.get_text())
    text = "".join(parts).strip()
    # Clean up whitespace
    text = re.sub(r" +", " ", text)
    return text


def _extract_translations(traduction_div):
    """Extract FR/ENG/NA translation pairs from a div.traduction table."""
    translations = []
    for row in traduction_div.find_all("tr"):
        cells = row.find_all(["th", "td"])
        entry = {}
        i = 0
        while i < len(cells) - 1:
            header = cells[i].get_text(strip=True).upper()
            value = cells[i + 1].get_text(strip=True)
            if header == "FR":
                entry["fr"] = value
            elif header in ("ENG", "EN"):
                entry["en"] = value
            elif header == "NA":
                entry["na"] = value
            i += 2
        if entry:
            translations.append(entry)
    return translations


def load_log():
    """Load or create the scraping log."""
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return {"extracted": {}, "errors": {}, "started": time.strftime("%Y-%m-%d %H:%M:%S")}


def save_log(log):
    """Save the scraping log."""
    log["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def run_extraction(session, subcategory_filter=None, resume=False, force=False):
    """Extract term definitions to structured markdown files."""
    if not INVENTORY_FILE.exists():
        print("ERROR: No URL inventory found. Run discovery first:")
        print("  python tools/data/dicobat_scraper.py discover")
        sys.exit(1)

    with open(INVENTORY_FILE) as f:
        inventory = json.load(f)

    terms = inventory["terms"]
    log = load_log()

    # Filter by subcategory if requested
    if subcategory_filter:
        terms = [t for t in terms if t["subcategory_id"] == subcategory_filter]
        print(f"Filtered to subcategory {subcategory_filter}: {len(terms)} terms")

    # Skip already extracted if resuming
    if resume:
        already_done = set(log.get("extracted", {}).keys())
        terms = [t for t in terms if str(t["id"]) not in already_done]
        print(f"Resuming: {len(already_done)} already done, {len(terms)} remaining")

    if not terms:
        print("Nothing to extract.")
        return

    print(f"\n{'='*60}")
    print(f"DICOBAT EXTRACTION: {len(terms)} terms")
    print(f"{'='*60}\n")

    current_theme = None
    theme_count = 0

    for i, term in enumerate(terms):
        # Theme progress header
        if term["theme_slug"] != current_theme:
            if current_theme:
                print(f"  ✓ {current_theme}: {theme_count} terms extracted\n")
            current_theme = term["theme_slug"]
            theme_count = 0
            print(f"Theme: {current_theme}")

        # Build output path
        theme_dir = SOURCE_DIR / slugify(term["theme_slug"])
        theme_dir.mkdir(parents=True, exist_ok=True)
        output_file = theme_dir / f"{term['slug']}.md"

        # Skip if file already exists (unless --force)
        if output_file.exists() and resume and not force:
            log["extracted"][str(term["id"])] = {
                "file": str(output_file.relative_to(PROJECT_ROOT)),
                "skipped": True,
            }
            continue

        print(f"  [{i+1}/{len(terms)}] {term['name']}", end="", flush=True)

        soup = fetch_page(session, term["url"])
        if not soup:
            log["errors"][str(term["id"])] = {
                "name": term["name"],
                "url": term["url"],
                "error": "fetch_failed",
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            print(" ✗ FAILED")
            save_log(log)
            continue

        # Check if the definition area has actual content
        definition_div = soup.find("div", id="definition")
        if not definition_div or not definition_div.get_text(strip=True):
            log["errors"][str(term["id"])] = {
                "name": term["name"],
                "url": term["url"],
                "error": "empty_content",
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            print(" ✗ EMPTY (session may have expired)")
            save_log(log)
            continue

        # Parse and save
        markdown = parse_term_page(soup, term)
        output_file.write_text(markdown, encoding="utf-8")

        log["extracted"][str(term["id"])] = {
            "name": term["name"],
            "file": str(output_file.relative_to(PROJECT_ROOT)),
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        theme_count += 1
        print(" ✓")

        # Save log every 10 terms
        if (i + 1) % 10 == 0:
            save_log(log)

    # Final theme summary
    if current_theme:
        print(f"  ✓ {current_theme}: {theme_count} terms extracted\n")

    save_log(log)

    # Print summary
    extracted_count = len([v for v in log["extracted"].values() if not v.get("skipped")])
    error_count = len(log["errors"])
    print(f"\n{'='*60}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"Extracted: {extracted_count}")
    print(f"Errors:    {error_count}")
    if error_count > 0:
        auth_errors = sum(1 for v in log["errors"].values() if v.get("error") == "auth_required")
        fetch_errors = error_count - auth_errors
        if auth_errors:
            print(f"  - Auth required: {auth_errors} (check your cookies)")
        if fetch_errors:
            print(f"  - Fetch failed:  {fetch_errors}")
    print(f"Output:    {SOURCE_DIR}")
    print(f"Log:       {LOG_FILE}")
    print()


def slugify(text):
    """Simple slugify for directory names."""
    return re.sub(r"[^a-zA-Z0-9-]", "-", text).strip("-").lower()


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(description="Dicobat Online Scraper")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # discover
    subparsers.add_parser("discover", help="Discover all theme/subcategory/term URLs")

    # extract
    extract_parser = subparsers.add_parser("extract", help="Extract term definitions")
    extract_parser.add_argument(
        "--subcategory", type=int, default=None,
        help="Only extract terms from this subcategory ID"
    )
    extract_parser.add_argument(
        "--resume", action="store_true",
        help="Skip already-extracted terms"
    )
    extract_parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing files (e.g., to fix encoding)"
    )

    # stats
    subparsers.add_parser("stats", help="Show inventory/extraction stats")

    args = parser.parse_args()

    if args.command == "discover":
        session = make_session(cookies_required=False)
        run_discovery(session)

    elif args.command == "extract":
        session = make_session(cookies_required=True)
        run_extraction(session, subcategory_filter=args.subcategory, resume=args.resume, force=args.force)

    elif args.command == "stats":
        if INVENTORY_FILE.exists():
            with open(INVENTORY_FILE) as f:
                inv = json.load(f)
            print("URL Inventory:")
            print(f"  Themes:        {inv['stats']['theme_count']}")
            print(f"  Subcategories: {inv['stats']['subcategory_count']}")
            print(f"  Unique terms:  {inv['stats']['unique_terms']}")
            print(f"  Discovered:    {inv['stats']['discovery_date']}")
        else:
            print("No inventory yet. Run: python tools/data/dicobat_scraper.py discover")

        if LOG_FILE.exists():
            with open(LOG_FILE) as f:
                log = json.load(f)
            print(f"\nExtraction log:")
            print(f"  Extracted: {len(log.get('extracted', {}))}")
            print(f"  Errors:    {len(log.get('errors', {}))}")
            print(f"  Updated:   {log.get('last_updated', 'never')}")
        else:
            print("No extraction log yet.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
