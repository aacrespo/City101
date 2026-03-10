import { useState } from "react";

const sites = [
  { id:1, name:"CHUV Night Staff Dispersal Arc",
    tag:"1,500 night workers dispersing to 32 residential areas — cheaper neighbourhoods have worst nocturnal transport",
    type:"staff_access", urg:"critical", km:60,
    swing:"1,500 CHUV night shift workers (nurses finish 23:00/07:00, urgences 24h). Staff who can afford to live near CHUV (Flon, Cour: CHF 80-95k) have 6-7 nocturnal stops. Staff who live where they can afford (Renens CHF 56-58k, Prilly CHF 66k, Bussigny CHF 72k, Ecublens CHF 70k) have 0-2 nocturnal stops.",
    res:[
      "Renens — 22,252 pop, CHF 56-58k income, 2 nocturnal stops, 3-3.4km from CHUV",
      "Prilly — 12,426, CHF 66k, 2 noct, 1.9km",
      "Bussigny — 6,472, CHF 72k, 0 noct, 6.0km",
      "Ecublens — 11,476, CHF 70k, 2 noct, 3.9km",
      "Préverenges — 5,721, CHF 82k, 0 noct, 6.7km",
      "Pierre-de-Plan — 8,000, CHF 60k, 2 noct, 2.6km (cheapest in Lausanne)"
    ],
    work:["CHUV — 12,000 day / 1,500 night","Clinique La Source — 200 night","Clinique Bois-Cerf — 150 night","Hospital Beaumont — linked to CHUV","CHUV-HUG pharma platform Bussigny — 80 night (supply chain)"],
    night:"The income-transport paradox: CHUV's cheapest nearby housing (Renens CHF 56k, Pierre-de-Plan CHF 60k, Sébeillon CHF 60k, Bellevaux CHF 60k) has 2-5 nocturnal stops — all Noctambus Fri/Sat only. Mon-Thu at 23:00 or 07:00, a nurse living in Renens (3.4km, CHF 56k) has zero transport. A nurse living in Flon (0.9km, CHF 80k) can walk. The horizontal elevator is an equity issue.",
    route:"CHUV → Sallaz → Pierre-de-Plan → Prilly → Renens → Bussigny", dist:7,
    lat:46.525, lon:6.620,
    why:"This is the corridor's most powerful healthcare story. 1,500 night workers dispersing from a single point. The data shows a direct correlation between housing affordability and transport access: cheaper neighbourhoods = fewer nocturnal stops. A nurse earning CHF 56k in Renens is stranded Mon-Thu. A doctor earning CHF 95k in Cour can walk. The horizontal elevator doesn't just move people — it corrects an equity failure in the healthcare system.",
    sigs:["1,500 night staff","income-transport paradox","Mon-Thu gap","CHF 56k vs 95k"] },

  { id:2, name:"Rennaz Hospital Island",
    tag:"400 night staff, 2.1km from rail, 0 nocturnal transport, 2.6★ — the corridor's worst-connected hospital",
    type:"staff_access", urg:"critical", km:89,
    swing:"Rennaz day/night ratio 2.29× (2nd highest on corridor). Hospital inflates daytime population by 1,448 people. 44,149m² of hospital buildings — largest health building footprint outside Geneva and Lausanne. Night staff live: Montreux 2.1km, Territet 1.5km, Villeneuve 3.8km, Vevey 7.6-7.9km, La Tour 5.8-6.3km.",
    res:[
      "Montreux-Centre — 8,000, 2.1km (6 nocturnal — but VMCV N290 only Fri/Sat)",
      "Territet/Glion — 3,000, 1.5km (4 noct Fri/Sat)",
      "Vernex/Châtelard — 4,000, 1.8km (48% foreign, CHF 65k)",
      "Haut-Montreux — 5,574, 2.2km (only 2 noct)",
      "Villeneuve — 3,500, 3.8km (only 1 noct, 62% car)",
      "Vevey — 20,159, 7.6-7.9km (where many specialists likely live)"
    ],
    work:["HRC Rennaz — 2,000 day / 400 night","PharmaRennaz — on-call","HRC Vevey Providence — 800 day (old site, 0.5km from rail)","Clinical Valmont Glion — rehab, shifts on mountainside"],
    night:"Built in 2019 to replace the old Vevey Providence and Montreux sites. The new hospital was placed at Rennaz for land availability — but 2.1km from rail, with 0 nocturnal transport and only 2 shared mobility stations. Staff note: 'car only.' Google rating 2.6★ (lowest hospital on corridor) — partly access frustration. The old Vevey site was 0.5km from La Tour-de-Peilz station.",
    route:"Vevey → La Tour → Montreux → Territet → Villeneuve → Rennaz HRC", dist:10,
    lat:46.435, lon:6.938,
    why:"A textbook case of healthcare access failure. When HRC moved from central Vevey (0.5km from rail) to Rennaz (2.1km from rail), it traded centrality for space. 400 night staff now drive. Patients from Montreux/Villeneuve who don't drive can't easily reach the ER. The 2.6★ rating is the data screaming. A horizontal elevator to Rennaz is literally a lifeline — for staff getting home and patients getting to care.",
    sigs:["400 night car-only","2.1km from rail","2.6★ (lowest)","44,149m² health buildings"] },

  { id:3, name:"Epalinges Medical Hill",
    tag:"3.4km from rail, 3.3★ — medical satellite above Lausanne with 67,736 residents in catchment",
    type:"patient_access", urg:"high", km:66,
    swing:"Centre médical d'Epalinges: 3.4km from Lausanne-Flon. Only 1 nocturnal stop <2km (Sallaz N4, 1.6km, Fri/Sat only). 19 shared mobility stations <1km. 4 hospital buildings (1,256m²). Catchment: 67,736 people in Lausanne's northern quarters.",
    res:[
      "Sallaz/Vennes — 12,000, 2.2km downhill (CHF 62k, 50% foreign)",
      "Pierre-de-Plan/Boveresses — 8,000, 1.6km (CHF 60k, 52% foreign)",
      "Pontaise/Blécherette — 8,000, 2.5km (CHF 65k, 45% foreign)",
      "Chailly/Rovéréaz — 9,000, 2.6km",
      "Vers-chez-les-Blanc — 2,000, 2.3km (Agriculture prof, 0 nocturnal, 3 mob)"
    ],
    work:["Centre médical Epalinges — 3.3★","→ CHUV 2.5km downhill","→ Hospital Beaumont 1.3km from Flon (4.8★)"],
    night:"Epalinges has 2,060 residential buildings but only 197 work buildings (7.4%). The medical centre serves the entire northern Lausanne heights — communities like Pierre-de-Plan (CHF 60k, 52% foreign), Sallaz (CHF 62k, 50% foreign) that are among Lausanne's most diverse and least affluent. These residents need to travel downhill for most healthcare. A horizontal elevator connecting Epalinges to CHUV and the rail network would serve both staff and patients.",
    route:"Epalinges med centre → Sallaz → CHUV → Lausanne-Flon", dist:4,
    lat:46.543, lon:6.667,
    why:"Lausanne's northern heights are where the cheapest housing meets the worst transport. The medical centre at Epalinges serves a catchment of 67,736 people — many in diverse, lower-income quarters. Getting from Epalinges to CHUV (for specialist referrals) or to the rail network means going downhill with limited options. This is a patient access problem as much as a staff problem.",
    sigs:["3.4km from rail","67.7k catchment","3.3★","7.4% work buildings"] },

  { id:4, name:"Morges Hospital Gap",
    tag:"300 night staff stranded — 1.4km from rail, 3.0★ (worst-rated hospital on corridor), 19% elderly in catchment",
    type:"staff_access", urg:"high", km:48,
    swing:"EHC Hospital Morges: 1.4km from station. Rating 3.0★. 300 night staff 'stranded after last train.' 7 shared mobility <1km. Nocturnal: 2 stops (Noctambus N2, Fri/Sat). Catchment 25,000 with 19% elderly (4,750 elderly people). 15 hospital buildings, 10,023m² total.",
    res:[
      "Morges centre — 6,000, 0.3km from hospital",
      "Morges résidentiel nord — 4,000, 1.0km",
      "Préverenges — 5,721, 2.7km (0 nocturnal)",
      "Lonay — 2,858, prison nearby",
      "→ Staff likely also from Lausanne area (25-30 min train, but last train ~00:30)"
    ],
    work:["EHC Hospital Morges — 300 night","Morges industrial zone — 250 night (2×8)","Permanence des Halles (4.0★) — walk-in clinic at station","CMM Medical Center (4.0★) — at station"],
    night:"Morges has an interesting healthcare cluster: the hospital (3.0★, 1.4km from rail) is separate from two well-rated clinics right at the station (4.0★ each). The hospital is where the night shift happens — and where the transport fails. 300 staff stranded. La Côte's elderly (19% of 25,000 catchment = 4,750 people) rely on this hospital. 58% car dependency.",
    route:"Morges Gare → Permanence des Halles → Hôpital EHC → Préverenges → St-Prex", dist:6,
    lat:46.511, lon:6.498,
    why:"The worst-rated hospital on the corridor (3.0★) is also 1.4km from rail with 300 stranded night staff. Meanwhile, the walk-in clinics AT the station are rated 4.0★. Access shapes ratings. 4,750 elderly people in the catchment depend on this hospital. A horizontal elevator connecting the hospital to the station — and to the residential areas where elderly patients live — addresses both the staff transport gap and the patient access gap.",
    sigs:["3.0★ (worst hospital)","300 night stranded","4,750 elderly","1.4km from rail"] },

  { id:5, name:"Montreux–Glion Altitude Medicine",
    tag:"Clinique Valmont at 600m+ (4.5★ rehab) — staff on mountainside, 23% elderly in Montreux catchment",
    type:"patient_access", urg:"moderate", km:85,
    swing:"Clinical Valmont (Glion): 0.6km from Territet station but 600m+ altitude. 4.5★. Private rehab clinic. 2 shared mobility <1km. Territet: only 2 trains/hour. Montreux catchment: 23% elderly (6,137 people) — highest elderly percentage east of Geneva.",
    res:[
      "Territet/Glion — 3,000 (Education prof, 40% foreign)",
      "Montreux-Centre — 8,000 (Hospitality, 48% foreign)",
      "Haut-Montreux — 5,574 (Tourism, 38% foreign, 12 mob, 2 noct)",
      "Vernex/Châtelard — 4,000 (48% foreign, CHF 65k — lowest Montreux)"
    ],
    work:["Clinical Valmont — rehab, 4.5★, mountain clinic","Clinique Suisse Montreux — 4.5★","Swiss Riviera Medical Center","Quai Santé Montreux — 3.3★","HES-SO tourism school (includes health tourism training)"],
    night:"Montreux has the highest elderly proportion east of Geneva (23%, 6,137 people). The town has a dense medical cluster: 31 hospital buildings (12,470m²), plus Valmont on the heights. But Haut-Montreux (5,574 pop) has only 2 nocturnal stops and 12 shared mobility stations. A rehab patient at Valmont whose family lives in Montreux centre faces a steep climb with poor transport.",
    route:"Montreux Gare → Territet → Glion/Valmont (funicular) → connect to Villeneuve/Rennaz", dist:5,
    lat:46.425, lon:6.920,
    why:"Montreux's healthcare paradox: high-end medical facilities (two 4.5★ clinics) in a town where 23% of the population is elderly and 55% commute by car. Valmont on the mountainside is a premier rehab facility — but getting patients and families up there, and getting staff home at night, is a vertical access problem. The funicular exists but doesn't run at night. This connects to the Rennaz story: Montreux's health ecosystem is split between lake (HRC Rennaz) and mountain (Valmont) with the town trapped between.",
    sigs:["23% elderly (highest east)","Valmont 600m+","4.5★ rehab","31 health buildings"] },

  { id:6, name:"Vevey–La Tour Elderly Care Corridor",
    tag:"20-22% elderly, 4 medical facilities, Riviera Providence hospital 0.5km from rail — the accessible counterpart to Rennaz",
    type:"patient_access", urg:"high", km:80,
    swing:"Vevey-La Tour catchment: 20-22% elderly (highest density: Burier 22%, La Tour 21%, Vevey 20%). 4 medical facilities within 1km of rail: HRC Vevey Providence (3.7★), Medical Center Gare (3.3★), Medical Home (4.1★), Medbase (3.6★). Contrast with Rennaz (2.1km from rail, 2.6★).",
    res:[
      "La Tour-de-Peilz — 12,148, 21% elderly (2,537 elderly), 58% car",
      "Vevey — 20,159, 20% elderly (3,939 elderly), 52% car",
      "Corsier-sur-Vevey — 3,468 hillside (15 health buildings, 3,880m²)",
      "Corseaux — 2,378 (0 nocturnal, 3 mob, 1.66× ratio)",
      "Chardonne — 2,958 (0 nocturnal, 1 mob, hillside)"
    ],
    work:["HRC Vevey Providence — 800 day (old hospital, still active for some services)","Medical Center Gare Vevey — at station","Medical Home Vevey — 4.1★","Medbase Vevey — near station","Nestlé HQ — 4,000 (adjacent, employees use these facilities)"],
    night:"The Vevey–La Tour medical corridor is rail-accessible (0-0.5km) — the opposite of Rennaz. But the hillside communes (Corsier: 15 health buildings; Corseaux: 0 nocturnal; Chardonne: 1 shared mobility) are disconnected from it. 6,476 elderly residents in the core catchment. Vevey hotels/restaurants produce 80 night workers who finish at 23:30 — some are likely older workers in the hospitality sector.",
    route:"Chardonne (hill) → Corseaux → Corsier → La Tour → Vevey Gare medical cluster", dist:5,
    lat:46.462, lon:6.843,
    why:"This is the counterexample to Rennaz — a healthcare cluster that IS accessible by rail. The lesson: connect the hillside elderly communes (Corsier, Corseaux, Chardonne) DOWN to it. 6,476 elderly people, many in hillside villages with zero nocturnal transport. A horizontal elevator from the hills to the Vevey medical rail hub solves the access gap that exists for the elderly population above the lake.",
    sigs:["6,476 elderly","4 facilities at rail","hillside disconnect","Rennaz counterpoint"] },

  { id:7, name:"Nyon Hospital + Genolier Hilltop",
    tag:"200 hospital night staff + 150 on hilltop clinic (0 nocturnal, 3.6km from rail) — La Côte's split healthcare",
    type:"staff_access", urg:"high", km:25,
    swing:"GHOL Nyon Hospital: 0.7km from rail, 3.4★, 200 night staff. Clinique de Genolier: 3.6km from rail, 0 nocturnal transport — 150 night staff 'by car only.' Together: 350 healthcare night workers. 47 health buildings in Nyon (17,525m²). 18% elderly (4,162 people). 56% car.",
    res:[
      "Nyon centre — 8,000, 42% foreign, 0.7km from hospital",
      "Nyon-Colovray — 4,629, 45% foreign (highest Nyon), south side",
      "Nyon-Changins — 5,000, north side",
      "→ Genolier hilltop: wealthy, no rail, no nocturnal"
    ],
    work:["GHOL Nyon Hospital — 200 night","Clinique de Genolier — 150 night, 3.6km from rail, hilltop","Zone Asse industrial — 300 night (adjacent)","16 hospital buildings in Prangins (3,350m² — psychiatric facility)"],
    night:"La Côte's healthcare is split between the lakeside (Nyon hospital, rail-accessible) and the hilltop (Genolier, car-only). Genolier clinic staff are among the most isolated night workers on the corridor: 3.6km from rail, zero nocturnal transport, on a hill above the vineyards. Plus Prangins has 16 hospital buildings (psychiatric) — another healthcare node slightly off the rail spine.",
    route:"Nyon Gare → GHOL Hospital → Prangins psychiatric → (hill) → Genolier clinic", dist:6,
    lat:46.383, lon:6.237,
    why:"La Côte's healthcare geography mirrors its residential geography: split between lake and hill. 350 night healthcare workers total — 200 at the accessible lakeside hospital, 150 at the inaccessible hilltop clinic. A horizontal elevator connecting Genolier down to Nyon would solve the most extreme healthcare worker isolation on the corridor. The Prangins psychiatric facility adds a sensitive patient access dimension.",
    sigs:["350 health night","Genolier 3.6km hilltop","Prangins psychiatric","18% elderly"] },

  { id:8, name:"Lavaux Healthcare Desert",
    tag:"7,121 residents, 20-24% elderly, nearest hospital 4.5-8km — UNESCO zone with zero medical infrastructure",
    type:"patient_access", urg:"moderate", km:72,
    swing:"Lavaux communes (Rivaz, St-Saphorin, Riex, Épesses, Grandvaux, Villette, Cully): combined 7,121 residents. Elderly: Rivaz 24%, St-Saphorin 22%, Épesses/Grandvaux/Cully 20%. Nearest hospital: 4.5-8km away. 68-72% car. Zero medical buildings in Rivaz, Riex, Épesses, St-Saphorin, Villette, Grandvaux (per buildings dataset).",
    res:[
      "Rivaz — 398, 24% elderly (96 elderly), 72% car, 1 mob, 0 noct",
      "Grandvaux — 2,451, 20% elderly (490 elderly), 68% car, 2 mob, 0 noct",
      "Cully — 2,074, 20% elderly (415 elderly), 68% car, 1 mob, 0 noct",
      "Épesses — 345, 20% elderly, 68% car, 1 mob, 0 noct",
      "Puidoux (above) — 3,156, 20% elderly, 70% car, 7.3km to hospital"
    ],
    work:["Zero healthcare employment in Lavaux","→ 4.5-8km to Vevey medical cluster","→ 6.8-8km to CHUV/Lausanne","Bourg-en-Lavaux has 6 health buildings (3,928m²) — nearest medical presence"],
    night:"A healthcare desert in a UNESCO World Heritage landscape. 1,500+ elderly people scattered across 7 tiny communes with zero medical infrastructure, 68-72% car dependency, zero nocturnal transport, and zero shared mobility. If an 80-year-old in Rivaz needs to reach the ER at 3am, there is literally nothing — no transport, no medical facility, no shared mobility. The closest ER is Vevey (4.5km) or Rennaz (10km, the car-only hospital).",
    route:"Puidoux/Chexbres → Rivaz → Épesses → Riex → Cully → Grandvaux → (to Lausanne or Vevey medical)", dist:12,
    lat:46.493, lon:6.735,
    why:"The most vulnerable healthcare population on the corridor. 1,500+ elderly people in UNESCO-protected vineyard villages with zero medical infrastructure, zero nocturnal transport, and car dependency above 68%. A horizontal elevator through Lavaux isn't just about commuters — it's about keeping elderly residents connected to healthcare. You can't build a clinic in a UNESCO zone, but you can build the lightest possible transport to reach one.",
    sigs:["24% elderly Rivaz","0 medical buildings","68-72% car","UNESCO constraint"] },
];

const typeColors = {
  staff_access: { border:"#ef5350", badge:"#b71c1c", accent:"#ef9a9a", bg:"#0d0505" },
  patient_access: { border:"#42A5F5", badge:"#0D47A1", accent:"#90CAF9", bg:"#050a0d" }
};

const uDot = { critical:"●●●", high:"●●○", moderate:"●○○" };
const uOrd = { critical:0, high:1, moderate:2 };

export default function App() {
  const [sel, setSel] = useState(null);
  const [filt, setFilt] = useState("all");
  const [sort, setSort] = useState("urgency");

  let list = filt === "all" ? [...sites] : sites.filter(s => s.type === filt);
  if (sort === "urgency") list.sort((a,b) => uOrd[a.urg] - uOrd[b.urg] || a.km - b.km);
  else list.sort((a,b) => a.km - b.km);

  return (
    <div style={{ fontFamily:"'Courier New',monospace", background:"#020202", color:"#bbb", minHeight:"100vh", padding:"20px 14px" }}>
      <div style={{ maxWidth:1000, margin:"0 auto" }}>
        <div style={{ marginBottom:24 }}>
          <div style={{ fontSize:9, letterSpacing:5, color:"#2a2a2a", marginBottom:3 }}>CITY101 · FLOW OF LIFE · HEALTHCARE LENS</div>
          <h1 style={{ fontSize:22, fontWeight:400, color:"#fff", margin:"0 0 4px" }}>
            8 Healthcare Sites — Staff Access + Patient Access
          </h1>
          <p style={{ fontSize:10, color:"#444", margin:0, maxWidth:700, lineHeight:1.5 }}>
            Cross-referenced: 23 hospitals, 5,490 healthcare night workers, 218k buildings (incl. 608 health buildings), elderly demographics, pharmacy locations, nocturnal transport, and the income-transport paradox.
          </p>
          <div style={{ marginTop:10, padding:8, border:"1px solid #1a1a1a", fontSize:9, color:"#555", lineHeight:1.6 }}>
            <span style={{ color:"#ef5350" }}>■</span> STAFF ACCESS — healthcare workers who can't get home after night shifts<br/>
            <span style={{ color:"#42A5F5" }}>■</span> PATIENT ACCESS — populations disconnected from medical facilities
          </div>
        </div>

        <div style={{ display:"flex", gap:5, marginBottom:14, flexWrap:"wrap", alignItems:"center" }}>
          {[["all","ALL 8"],["staff_access","■ STAFF ACCESS"],["patient_access","■ PATIENT ACCESS"]].map(([v,l])=>(
            <button key={v} onClick={()=>setFilt(v)} style={{
              padding:"3px 9px", fontSize:9, letterSpacing:1.2,
              border:filt===v?"1px solid #fff":"1px solid #151515",
              background:filt===v?"#fff":"transparent", color:filt===v?"#000":"#3a3a3a", cursor:"pointer"
            }}>{l}</button>
          ))}
          <div style={{flex:1}}/>
          {[["urgency","URGENCY"],["corridor","POSITION"]].map(([v,l])=>(
            <button key={v} onClick={()=>setSort(v)} style={{
              padding:"3px 7px", fontSize:9, border:"none", background:"none",
              color:sort===v?"#fff":"#2a2a2a", cursor:"pointer",
              textDecoration:sort===v?"underline":"none", textUnderlineOffset:3
            }}>{l}</button>
          ))}
        </div>

        <div style={{ display:"flex", flexDirection:"column", gap:4 }}>
          {list.map(s=>{
            const o = sel===s.id;
            const t = typeColors[s.type];
            return <div key={s.id} style={{
              border:`1px solid ${o?t.border:"#0e0e0e"}`, background:o?t.bg:"#060606", transition:"all 0.15s"
            }}>
              <div onClick={()=>setSel(o?null:s.id)} style={{ padding:"8px 12px", display:"flex", alignItems:"center", gap:8, cursor:"pointer" }}>
                <div style={{ width:4, height:4, borderRadius:"50%", background:t.border, flexShrink:0 }}/>
                <div style={{ flex:1, minWidth:0 }}>
                  <div style={{ display:"flex", alignItems:"center", gap:5, flexWrap:"wrap" }}>
                    <span style={{ fontSize:8, padding:"1px 4px", background:t.badge, color:"#fff", letterSpacing:1 }}>
                      {s.type==="staff_access"?"STAFF":"PATIENT"}
                    </span>
                    <span style={{ fontSize:8, color:"#3a3a3a" }}>{uDot[s.urg]} {s.urg.toUpperCase()}</span>
                    <span style={{ fontSize:8, color:"#222" }}>km{s.km}</span>
                  </div>
                  <div style={{ fontSize:12, fontWeight:600, color:"#ddd", marginTop:1, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{s.name}</div>
                  <div style={{ fontSize:9, color:"#4a4a4a", fontStyle:"italic" }}>{s.tag}</div>
                </div>
                <div style={{ fontSize:12, color:"#222", transform:o?"rotate(45deg)":"none", transition:"transform 0.12s", flexShrink:0 }}>+</div>
              </div>
              {o && (
                <div style={{ padding:"0 12px 12px", borderTop:"1px solid #0c0c0c" }}>
                  <div style={{ display:"flex", gap:3, flexWrap:"wrap", padding:"6px 0 10px" }}>
                    {s.sigs.map((sig,i)=>(
                      <span key={i} style={{ fontSize:7, padding:"1px 5px", border:`1px solid ${t.border}30`, color:t.accent }}>{sig}</span>
                    ))}
                  </div>
                  <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12 }}>
                    <div>
                      <S l="THE SITUATION" c={t.accent} t={s.swing}/>
                      <S l="RESIDENTIAL / CATCHMENT" c={t.accent}>{s.res.map((r,i)=><L key={i}>{r}</L>)}</S>
                      <S l="HEALTHCARE FACILITIES" c={t.accent}>{s.work.map((w,i)=><L key={i}>{w}</L>)}</S>
                    </div>
                    <div>
                      <S l="THE NIGHT / ACCESS GAP" c={t.accent} t={s.night}/>
                      <S l="PROPOSED ROUTE" c={t.accent}>
                        <div style={{ fontSize:10, color:"#fff", fontWeight:500 }}>{s.route}</div>
                        <div style={{ fontSize:8, color:"#333", marginTop:1 }}>{s.dist}km</div>
                      </S>
                      <div style={{ padding:7, marginTop:4, background:"#030303", border:`1px solid ${t.border}15` }}>
                        <div style={{ fontSize:7, color:t.accent, letterSpacing:2, marginBottom:2 }}>WHY THIS SITE</div>
                        <div style={{ fontSize:9, color:"#aaa", lineHeight:1.5 }}>{s.why}</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>;
          })}
        </div>

        <div style={{ marginTop:24, padding:"12px 0", borderTop:"1px solid #0e0e0e" }}>
          <div style={{ fontSize:8, letterSpacing:3, color:"#2a2a2a", marginBottom:8 }}>HEALTHCARE CORRIDOR FINDINGS</div>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:10 }}>
            {[
              ["5,490","#ef5350","Total healthcare night workers"],
              ["23","#42A5F5","Hospitals / clinics on corridor"],
              ["608","#fff","Health buildings (218k dataset)"],
              ["18-24%","#90CAF9","Elderly population range"]
            ].map(([n,c,d],i)=>(
              <div key={i}>
                <div style={{ fontSize:16, color:c, fontWeight:300 }}>{n}</div>
                <div style={{ fontSize:8, color:"#444" }}>{d}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop:12, fontSize:9, color:"#333", lineHeight:1.6 }}>
            Two patterns emerge: (1) Staff access — an income-transport paradox where nurses who earn less live further from hospitals with worse nocturnal transport. (2) Patient access — elderly populations in hillside/vineyard communes disconnected from medical facilities by altitude and car dependency. The horizontal elevator addresses both: it moves healthcare workers to hospitals at night, and patients to hospitals by day.
          </div>
        </div>
      </div>
    </div>
  );
}

function S({l,c,t,children}){
  return <div style={{marginBottom:8}}>
    <div style={{fontSize:7,color:c,letterSpacing:2,marginBottom:2}}>{l}</div>
    {t&&<div style={{fontSize:9,color:"#999",lineHeight:1.5}}>{t}</div>}
    {children}
  </div>;
}
function L({children}){
  return <div style={{fontSize:8,color:"#777",lineHeight:1.5,paddingLeft:5,borderLeft:"1px solid #151515"}}>{children}</div>;
}
