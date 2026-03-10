import { useState } from "react";

const sites = [
  // === TIER 1: CRITICAL (5) ===
  { id:1, name:"Ecublens ↔ Lausanne West", tag:"Campus flood — 30k pour in, ghost at night", type:"daytime", urg:"critical", km:62,
    swing:"+18,786 day (ratio 2.48×, highest)", res:["Renens-Gare 10k, 2.0km","Renens indust. 12k, 2.5km","Prilly 12k, 3.1km","Bussigny 6.5k, 3.6km"],
    work:["EPFL — 16k","UNIL — 14k"], night:"Bussigny: 800 night workers, 0 nocturnal transport <2km. Migros 350 finish 06:00.",
    route:"Bussigny → EPFL → Renens → Prilly → Malley", dist:8, lat:46.519, lon:6.567,
    why:"Biggest population swing on corridor. 30k tidal wave by day, 800 stranded by night.", sigs:["2.48× ratio","30k jobs","800 night","remote desert"] },
  { id:2, name:"Geneva North Industrial Belt", tag:"4,600 night workers — 3 venues", type:"nocturnal", urg:"critical", km:8,
    swing:"80k res / 30.5k jobs / 4,600 night", res:["Vernier 10k","Meyrin 14k","Aïre/Lignon 13k"],
    work:["ZIPLO 10k","ZIMEYSA 6k","ZIMEYSAVER 5k","Airport 8k (+3k night)"],
    night:"Airport 3k night. Post 600 (02:00-05:00). DHL 300. Port Franc 500. 12k frontaliers.",
    route:"Vernier → Blandonnet → ZIMEYSA → Meyrin → CERN → Airport", dist:7, lat:46.223, lon:6.093,
    why:"Corridor's biggest nocturnal zone. 4,600 workers when nothing runs.", sigs:["4,600 night","3 venues","12k frontaliers","54% car"] },
  { id:7, name:"Lancy–Pont-Rouge ↔ Onex/ZIPLO", tag:"Commuter 4.04 — empties on weekends", type:"daytime", urg:"critical", km:4,
    swing:"10,100 weekday vs 2,500 weekend (4×)", res:["Onex 19k (3.6km cowork)","Petit-Lancy 12k","Carouge-Sud 15k","Plan-les-Ouates 10k"],
    work:["Pont-Rouge 8k","ZIPLO 10k","Acacias 5k"],
    night:"Lancy-Bachet: 700 shift. Police: 500 24h. Zero workspaces in industrial belt.",
    route:"Onex → Lancy → Pont-Rouge → Acacias → ZIPLO", dist:6, lat:46.183, lon:6.117,
    why:"Most extreme Geneva commuter (4×). 65k within 2km. Onex: biggest remote work desert.", sigs:["commuter 4.04","19k no cowork","1.2k night","ZIPLO 10k"] },
  { id:10, name:"Lausanne Perpendicular: Lake ↔ Hill", tag:"5.8km / 250m altitude — 127k split", type:"daytime", urg:"critical", km:65,
    swing:"127k from Ouchy (370m) to Vers-chez-les-Blanc (700m)", res:["Ouchy 6k (370m)","Sallaz 12k (590m)","Pontaise 8k (600m+)"],
    work:["Flon 15k","CHUV 12k","Gare 5k","8.4k frontaliers"],
    night:"CHUV: 1,500 night. M2 stops midnight. Firefighters: 120 24h.",
    route:"Ouchy → Gare → CHUV → Sallaz → Blécherette", dist:4, lat:46.525, lon:6.635,
    why:"Most topographic split. 250m gradient. Where 'horizontal' gets tested architecturally.", sigs:["5.8km spread","250m alt","1.5k CHUV","Vigie 2.9★"] },
  { id:18, name:"Crissier–Bussigny Night Belt", tag:"1,680 night workers — corridor's supply chain", type:"nocturnal", urg:"critical", km:58,
    swing:"Bussigny commuter 2.0. Crissier 5k retail/logistics day.", res:["Bussigny 6.5k","Crissier 5.5k","Renens 22k","Ecublens 11.5k"],
    work:["Bussigny Arc-en-Ciel 800 (3×8)","Renens/Crissier 600 (3×8)","Voxel 200 (24h)","CHUV-HUG pharma 80 (24h)"],
    night:"1,680 total. Pharma supply for hospitals, food for Migros, packages for morning. Zero nocturnal transport <2km.",
    route:"Renens → Crissier → Bussigny → Voxel", dist:5, lat:46.551, lon:6.550,
    why:"Invisible supply chain. 1,680 workers sorting/packaging/distributing through the night. Logistics lifeline.", sigs:["1,680 night","0 nocturnal","pharma chain","commuter 2.0"] },

  // === TIER 2: HIGH (9) ===
  { id:3, name:"Pully–Lutry → Lausanne", tag:"20k residents, 800 jobs — purest bedroom", type:"daytime", urg:"high", km:68,
    swing:"Jobs/pop 0.04 (lowest). 7% work buildings.", res:["Pully 8k","Chamblandes 5k","Lutry 4.6k"],
    work:["→ 3.9km Flon 15k","→ 3.6km CHUV 12k","→ 8.9km EPFL 16k"],
    night:"Zero night workers. Zero venues. CHUV nurses live here, finish 23:00/07:00.",
    route:"Lutry → Pully → Ouchy → CHUV/Flon", dist:6, lat:46.508, lon:6.68,
    why:"Purest bedroom community. Broken perpendicular: lake towns, hill jobs.", sigs:["jobs/pop 0.04","7% work bldgs","0 venues","perp. split"] },
  { id:4, name:"Morges–Rolle Gap", tag:"Hospital staff stranded — La Côte blind spot", type:"nocturnal", urg:"high", km:48,
    swing:"51.8k scattered across La Côte. Morges commuter 1.66.", res:["Morges 6k","Préverenges 5.7k","Rolle 4.5k"],
    work:["Hôpital La Côte 300 night","Morges 4k day","Industrial 2.5k"],
    night:"Hospital: 300 'stranded after last train.' Morges industrial 250 night. 2 venues. Zero nocturnal.",
    route:"Morges → Hôpital → Préverenges → St-Prex → Rolle", dist:18, lat:46.511, lon:6.498,
    why:"Longest gap GE–LS. Hospital 24h shifts, no way home.", sigs:["550 stranded","0 nocturnal","3.9km gap","58% car"] },
  { id:5, name:"Montreux–Rennaz Hospital", tag:"400 night staff — corridor's east dead end", type:"nocturnal", urg:"high", km:90,
    swing:"27.7k res. Car-only hospital.", res:["Montreux 12k","Villeneuve 5.8k","La Tour 12k"],
    work:["HRC Rennaz 400 night","Casino/bars 80 (02:00)","Boulangeries 25 (02:00)"],
    night:"Hospital 'no train, car only.' Rating 2.6★ (lowest). Built off-rail.",
    route:"Montreux → Territet → Villeneuve → Rennaz", dist:7, lat:46.435, lon:6.938,
    why:"New hospital off-rail = instant 400-worker gap. 2.6★ rating.", sigs:["400 stranded","2.6★","6km gap","car-only"] },
  { id:8, name:"Genève-Sécheron International", tag:"Commuter 4.53 — ghost on weekends", type:"daytime", urg:"high", km:6,
    swing:"2,900 wkday vs 640 wkend (4.53×)", res:["Sécheron 8k 50%foreign","Petit-Saconnex 15k 55%","Pâquis 14k 62%"],
    work:["ONU 10k","Sécheron orgs 5k","51k frontaliers GVA"],
    night:"International zone dead evenings/weekends. 62k+ residents around but zero connection after hours.",
    route:"Pâquis → Sécheron → Nations → Chambésy → Airport", dist:5, lat:46.2228, lon:6.1442,
    why:"Highest commuter index (4.53). Global workplace, dead zone evenings/weekends.", sigs:["commuter 4.53","51k frontaliers","62% foreign","weekend ghost"] },
  { id:9, name:"Gland–Rolle La Côte Gap", tag:"6.3km gap, 14k people, 4.5 tr/hr", type:"daytime", urg:"high", km:38,
    swing:"Gland 2.33 / Rolle 2.00. 62% car both.", res:["Gland 5.5k","Mont-sur-Rolle 3.2k (3.4km!)","Scattered villages 1.8×"],
    work:["Gland tech, 1.4k frontaliers","Rolle 4.6k daily","4.5 tr/hr Rolle"],
    night:"Zero everything between. Villages 1.8×+ ratio — empty because everyone drives away.",
    route:"Gland → Bursinel → Tartegnin → Rolle", dist:7, lat:46.443, lon:6.305,
    why:"Biggest La Côte gap. Car-dependent villages. Too spread for buses, too populated to ignore.", sigs:["6.3km gap","4.5 tr/hr","1.8× ratio","62% car"] },
  { id:12, name:"Founex–Nyon Gap", tag:"6.6km — longest gap, 28k between", type:"daytime", urg:"high", km:28,
    swing:"Nyon commuter 1.95. Coppet 60% car.", res:["Founex 4k (mob. desert)","Commugny 3.1k","Coppet 4.9k"],
    work:["→ Nyon 18k zone","3.4k frontaliers","60% car despite rail"],
    night:"Zero nocturnal Coppet–Nyon. Zero venues. Founex: 3 shared mobility stations.",
    route:"Coppet → Tannay → Mies → Founex → Nyon", dist:7, lat:46.375, lon:6.245,
    why:"Longest physical gap in rail spine. 28k people. Worst shared mobility.", sigs:["6.6km (longest)","28k pop","3 mob stations","60% car"] },
  { id:13, name:"Bernex — Stranded Southwest", tag:"10.6k residents — 0 venues, 0 coworking", type:"nocturnal", urg:"high", km:2,
    swing:"10,574 in complete isolation from Geneva services", res:["Bernex 10.6k, 35% foreign","→ 5.7km to coworking"],
    work:["→ 2.7km Pont-Rouge 8k","→ 3.1km ZIPLO 10k","→ 5.2km Acacias 5k"],
    night:"0 late venues <3km. 2 nocturnal stops <3km. After midnight: completely cut off from urban life.",
    route:"Bernex → Confignon → Onex → Pont-Rouge → ZIPLO", dist:5, lat:46.175, lon:6.077,
    why:"Most isolated residential in Geneva. Zero venues, coworking, or night life. The darkest pocket.", sigs:["0 venues 3km","5.7km cowork","2 nocturnal","35% foreign"] },
  { id:19, name:"Nyon Industrial + Hospital Night", tag:"730 night workers — hospital, pharma, hotels", type:"nocturnal", urg:"high", km:25,
    swing:"21.6k res. 56% car. 3.4k frontaliers.", res:["Nyon centre 8k","Nyon-Asse 4k","Nyon-Changins 5k","Nyon-Colovray 4.6k, 45% foreign"],
    work:["Hôpital Nyon SHN 200 night","Zone Asse industrial 300 (2×8)","Hôtels lac 30 (24h)","→ Genolier clinique 150 (24h, hillside)"],
    night:"730 night workers: hospital (200), industrial (300), Genolier clinic (150 in hills, no night transport), hotels (30). Hospital rated 3.4★.",
    route:"Nyon centre → Hôpital → Zone Asse → Prangins → Genolier (hill)", dist:8, lat:46.383, lon:6.237,
    why:"La Côte's only real urban centre, but 56% car dependency. 730 night workers including a hilltop clinic completely disconnected from rail.", sigs:["730 night","56% car","3.4k frontaliers","hilltop clinic"] },
  { id:20, name:"Lausanne Flon Nightlife Circuit", tag:"300 bar/club staff stranded Mon–Thu nights", type:"nocturnal", urg:"high", km:65,
    swing:"300 staff finish 02:00-04:00. Noctambus runs Fri/Sat ONLY.", res:["Centre/Flon 12k","Bourdonnette 8k","Valency 10k","Bellevaux 7k"],
    work:["Flon clubs/bars — 300 staff","CHUV night shift — 1,500","Beau-Rivage Palace — 25 (24h)"],
    night:"7 nocturnal stops within 2km — but ALL are Fri/Sat only (Noctambus). Monday–Thursday: 300 nightlife workers, 1,500 CHUV staff, and Lausanne's 12,000 Flon residents share a dead window of 00:30–05:00 with zero public transport.",
    route:"Flon → Bourdonnette → Sallaz → CHUV → Ouchy", dist:3, lat:46.520, lon:6.631,
    why:"Lausanne has nocturnal transport — but only on weekends. Weeknight gap: 300 bar staff, 1,500 hospital workers, and 47,000 residents in the inner city share the same 00:30–05:00 dead window Mon–Thu.", sigs:["300 night staff","Fri/Sat only","Mon-Thu gap","47k inner city"] },

  // === TIER 3: MODERATE (10) ===
  { id:6, name:"Versoix–Geneva International", tag:"13k residents, 6km to employer", type:"daytime", urg:"moderate", km:15,
    swing:"13.5k — most disconnected residential cluster", res:["Versoix résid. 6.5k, 6.3km to UN","Versoix centre 7k, 6.0km"],
    work:["→ 6km ONU 10k","→ 6.3km Sécheron 5k","→ 8km Banques 15k"],
    night:"Genolier 150 night. 1.9k frontaliers. Commuter 1.82.",
    route:"Versoix → Genthod → Bellevue → Sécheron → Nations", dist:8, lat:46.283, lon:6.163,
    why:"Most disconnected residential cluster — 6km+ to any employer.", sigs:["6km gap","commuter 1.82","1.9k frontaliers"] },
  { id:11, name:"Burier–La Tour Spine", tag:"Commuter 3.49 — tiny station, heavy lifting", type:"daytime", urg:"moderate", km:82,
    swing:"2,200 wkday vs 630 wkend. 4 tr/hr.", res:["La Tour 12.1k","Vevey 8k (2.1km)","Corsier 3.5k hillside"],
    work:["→ Nestlé 4k","→ Vevey 3.5k","→ Montreux 5k"],
    night:"Vevey bars 50 finish 01:00. Hotels 80 till 23:30. Casino 80 finish 02:00.",
    route:"Corsier → La Tour → Burier → Vevey", dist:5, lat:46.457, lon:6.870,
    why:"3rd highest commuter index. Carries hillside villages invisibly.", sigs:["commuter 3.49","4 tr/hr","hillside","80+ hosp. night"] },
  { id:14, name:"Thônex-Moillesulaz Border", tag:"27k at Geneva's eastern dead end", type:"daytime", urg:"moderate", km:5,
    swing:"27k at border cul-de-sac. 4.2km to station.", res:["Moillesulaz 5.8k 55% foreign","Thônex 9k","Chêne-Bougeries 12.2k"],
    work:["→ 3.2km Eaux-Vives 2.5k","→ 3.6km Uni 8k","→ 4.2km Banques 15k"],
    night:"1 nocturnal stop <3km. Border = hard wall. Top profession at border: 'Transport/Customs'.",
    route:"Chêne-Bougeries → Thônex → Moillesulaz → [France]", dist:4, lat:46.197, lon:6.210,
    why:"Eastern dead end where city meets France. 4.2km from a real station. Border creates wall.", sigs:["4.2km to station","27k pop","55% foreign","border wall"] },
  { id:15, name:"Allaman Hub — Ghost Station", tag:"5,200 daily pax from village of 646", type:"daytime", urg:"moderate", km:43,
    swing:"8× ridership/pop ratio. Commuter 2.0.", res:["Buchillon 698, 0.4km","Perroy 1.8k, 3.5km","Mont-sur-Rolle 3.2k, 4.8km","St-Prex 6k, 4.4km"],
    work:["St-Prex industrie 2k (4.7km)","→ Morges 4k (8km)","→ Lausanne 15k+ (20km)"],
    night:"Zero anything at night. Platform in vineyards. 5,200 daily converge by car from 6km arc.",
    route:"St-Prex → Lully → Allaman → Buchillon → Perroy → Mont-sur-Rolle", dist:8, lat:46.469, lon:6.395,
    why:"Ridership anomaly: 8× more passengers than residents. Secret funnel for La Côte villages — replace 5k car trips.", sigs:["8× anomaly","commuter 2.0","car funnel","0 night"] },
  { id:16, name:"Lavaux Vineyard Corridor", tag:"UNESCO, 7.1k — ratios up to 1.89×", type:"daytime", urg:"moderate", km:74,
    swing:"7 communes. Rivaz 1.89, St-Saphorin 1.89, Riex 1.87, Épesses 1.86.",
    res:["Grandvaux 2.5k","Cully 2.1k","Riex-Épesses-Rivaz-StSaphorin 1.6k total"],
    work:["Wine production only","→ LS 12km west","→ Vevey 5km east","Tourism seasonal"],
    night:"8 venues across Lavaux. 3–4.5 tr/hr. Lowest ridership (150-760). UNESCO = can't widen roads.",
    route:"Grandvaux → Villette → Cully → Riex → Épesses → Rivaz → St-Saphorin", dist:10, lat:46.493, lon:6.735,
    why:"Highest day/night ratios. UNESCO = no road expansion. Lightest infrastructure in most protected landscape.", sigs:["1.89× (highest)","UNESCO","3 tr/hr","68% car"] },
  { id:17, name:"Epalinges Medical Hill", tag:"3.4km from rail — medical satellite", type:"daytime", urg:"moderate", km:66,
    swing:"2,060 homes, 197 work bldgs (7.4%). 38 mob stations → no rail.", res:["Sallaz 12k, 2.2km","Pierre-de-Plan 8k, 1.6km","Chailly 9k, 2.6km"],
    work:["Centre médical Epalinges 3.3★","Beaumont du CHUV 1.3km","→ CHUV 2.5km downhill"],
    night:"Medical staff work shifts uphill. Nearest cowork 3.4km. 38 shared mobility but dead-ends at rail.",
    route:"Epalinges → Sallaz → CHUV → Flon", dist:4, lat:46.543, lon:6.667,
    why:"Medical satellite off-grid. Shared mobility exists but doesn't connect to rail spine.", sigs:["3.4km from rail","7.4% work","medical","38 mob dead-end"] },
  { id:21, name:"Satigny Agricultural Island", tag:"15% primary sector — zero shared mobility, 8.3km to coworking", type:"daytime", urg:"moderate", km:1,
    swing:"4,461 pop. Ratio 1.45. Viticulture commune.", res:["Satigny 4.5k, 15% primary sector"],
    work:["→ 2.4km CERN 3.5k","→ 3.6km ZIMEYSAVER 5k","→ 4.1km Blandonnet 4k"],
    night:"1 nocturnal stop <3km. Zero venues. Zero shared mobility. 8.3km to nearest coworking. 776 work buildings (mostly agricultural) vs 996 residential — but the work buildings are farms, not offices.",
    route:"Satigny → Meyrin → CERN → ZIMEYSAVER", dist:5, lat:46.213, lon:6.033,
    why:"The corridor's agricultural anomaly. 15% primary sector — highest by far. Zero micro-mobility. The horizontal elevator here connects wine country to CERN.", sigs:["15% primary","0 mobility","8.3km cowork","wine → CERN"] },
  { id:22, name:"Puidoux-Chexbres Hillside", tag:"5,460 pop, 68% car — hillside above Lavaux", type:"daytime", urg:"moderate", km:76,
    swing:"Combined 5.5k. 2 tr/hr. 7.3km to employer. 68% car.", res:["Puidoux 3.2k","Chexbres 2.3k"],
    work:["→ 7.3km Nestlé 4k","→ 5.2km Vevey 3.5k","→ 12km EPFL 16k"],
    night:"Zero nocturnal. Zero venues (1 in Chexbres). 5 shared mobility. 5.7km to coworking.",
    route:"Chexbres → Puidoux → Rivaz → Cully (connect to lakeside)", dist:5, lat:46.496, lon:6.760,
    why:"Hillside above Lavaux. 68% car — highest on corridor. 2 trains/hour. Connects the vineyard hill towns to the lakeside rail.", sigs:["68% car (highest)","2 tr/hr","7.3km to work","hillside"] },
  { id:23, name:"Genthod-Bellevue Lakeside", tag:"6,293 — 60% car, zero nocturnal, zero venues", type:"nocturnal", urg:"moderate", km:12,
    swing:"Genthod commuter 2.17. Bellevue 1.35. 60% car.", res:["Bellevue 3.4k","Genthod 2.9k, 40% foreign, Finance prof"],
    work:["→ 4.1km Nations 10k","→ 2.2km Sécheron 5k","→ Pregny-Chambésy orgs"],
    night:"Zero nocturnal transport. Zero venues. Genthod: wealthy commune (Finance prof), 40% foreign — international workers stranded after dinner.",
    route:"Genthod → Bellevue → Pregny-Chambésy → Sécheron", dist:4, lat:46.258, lon:6.155,
    why:"Wealthy lakeside communes with zero night infrastructure. International residents (40% foreign) completely cut off after midnight. Between Versoix (Site 6) and Sécheron (Site 8) — fills the gap.", sigs:["60% car","0 nocturnal","0 venues","40% foreign"] },
  { id:24, name:"Saint-Prex Isolated Village", tag:"6,047 pop — 4 tr/hr, zero nocturnal, zero venues", type:"nocturnal", urg:"moderate", km:51,
    swing:"Commuter 1.92. 64% car.", res:["St-Prex village 3k","St-Prex résidentiel 2k","St-Prex industrial 1k"],
    work:["St-Prex industrie 2k (0.7km)","→ 5km Morges 4k","→ 9km Rolle 2k"],
    night:"Zero nocturnal. Zero venues. 4 trains/hour. Between Morges (Site 4) and Allaman (Site 15) — the forgotten middle.",
    route:"Morges → Lonay-Préverenges → Saint-Prex → Allaman", dist:6, lat:46.482, lon:6.444,
    why:"Small town trapped between Morges and Allaman with minimal service. 64% car despite being on rail. Zero night life, zero transport after midnight. The in-between place.", sigs:["64% car","4 tr/hr","0 nocturnal","0 venues"] },
];

const tc = {
  daytime: { border:"#FF9800", badge:"#E65100", accent:"#FFB74D", bg:"#0d0b08" },
  nocturnal: { border:"#5C6BC0", badge:"#1A237E", accent:"#7986CB", bg:"#08091a" }
};
const uDot = { critical:"●●●", high:"●●○", moderate:"●○○" };
const uOrd = { critical:0, high:1, moderate:2 };

export default function App() {
  const [sel, setSel] = useState(null);
  const [filt, setFilt] = useState("all");
  const [sort, setSort] = useState("corridor");

  let list = filt === "all" ? [...sites] : sites.filter(s => s.type === filt);
  if (sort === "urgency") list.sort((a,b) => uOrd[a.urg] - uOrd[b.urg] || a.km - b.km);
  else list.sort((a,b) => a.km - b.km);

  const stats = {
    day: sites.filter(s=>s.type==="daytime").length,
    night: sites.filter(s=>s.type==="nocturnal").length,
    crit: sites.filter(s=>s.urg==="critical").length,
    high: sites.filter(s=>s.urg==="high").length,
  };

  return (
    <div style={{ fontFamily:"'Courier New',monospace", background:"#020202", color:"#bbb", minHeight:"100vh", padding:"20px 14px" }}>
      <div style={{ maxWidth:1000, margin:"0 auto" }}>
        <div style={{ marginBottom:24 }}>
          <div style={{ fontSize:9, letterSpacing:5, color:"#2a2a2a", marginBottom:3 }}>CITY101 · FLOW OF LIFE · A.02</div>
          <h1 style={{ fontSize:22, fontWeight:400, color:"#fff", margin:"0 0 4px" }}>24 Horizontal Elevator Sites</h1>
          <p style={{ fontSize:10, color:"#444", margin:0, maxWidth:700, lineHeight:1.5 }}>
            Cross-referenced from 15 datasets incl. 218k buildings, GTFS timetables, hourly ridership, station reviews, frontalier estimates, and shared mobility coverage.
          </p>
        </div>

        <div style={{ display:"flex", gap:5, marginBottom:14, flexWrap:"wrap", alignItems:"center" }}>
          {[["all",`ALL ${sites.length}`],["daytime",`☀ DAY (${stats.day})`],["nocturnal",`☽ NIGHT (${stats.night})`]].map(([v,l])=>(
            <button key={v} onClick={()=>setFilt(v)} style={{
              padding:"3px 9px", fontSize:9, letterSpacing:1.2,
              border:filt===v?"1px solid #fff":"1px solid #151515",
              background:filt===v?"#fff":"transparent", color:filt===v?"#000":"#3a3a3a", cursor:"pointer"
            }}>{l}</button>
          ))}
          <div style={{flex:1}}/>
          {[["corridor","POSITION"],["urgency","URGENCY"]].map(([v,l])=>(
            <button key={v} onClick={()=>setSort(v)} style={{
              padding:"3px 7px", fontSize:9, border:"none", background:"none",
              color:sort===v?"#fff":"#2a2a2a", cursor:"pointer",
              textDecoration:sort===v?"underline":"none", textUnderlineOffset:3
            }}>{l}</button>
          ))}
        </div>

        {/* Corridor */}
        <div style={{ position:"relative", height:32, marginBottom:20 }}>
          <div style={{ position:"absolute", top:14, left:0, right:0, height:1, background:"#1a1a1a" }}/>
          <div style={{ position:"absolute", left:0, top:1, fontSize:8, color:"#2a2a2a" }}>GE</div>
          <div style={{ position:"absolute", right:0, top:1, fontSize:8, color:"#2a2a2a" }}>VN</div>
          {sites.map(s=>{
            const pct = Math.min(97,Math.max(3,(s.km/95)*100));
            const c = tc[s.type].border;
            const act = sel===s.id;
            const vis = filt==="all"||s.type===filt;
            return <div key={s.id} onClick={()=>setSel(act?null:s.id)} style={{
              position:"absolute", left:`${pct}%`, top:10,
              width:act?11:7, height:act?11:7, borderRadius:"50%",
              background:act?"#fff":vis?c:"#111",
              border:act?`2px solid ${c}`:"none",
              cursor:"pointer", transform:`translateX(-${act?5.5:3.5}px)`,
              transition:"all 0.12s", zIndex:act?3:1, opacity:vis?1:0.15
            }} title={s.name}/>;
          })}
        </div>

        {/* Cards */}
        <div style={{ display:"flex", flexDirection:"column", gap:4 }}>
          {list.map(s=>{
            const o = sel===s.id;
            const t = tc[s.type];
            return <div key={s.id} style={{
              border:`1px solid ${o?t.border:"#0e0e0e"}`, background:o?t.bg:"#060606", transition:"all 0.15s"
            }}>
              <div onClick={()=>setSel(o?null:s.id)} style={{ padding:"8px 12px", display:"flex", alignItems:"center", gap:8, cursor:"pointer" }}>
                <div style={{ width:4, height:4, borderRadius:"50%", background:t.border, flexShrink:0 }}/>
                <div style={{ flex:1, minWidth:0 }}>
                  <div style={{ display:"flex", alignItems:"center", gap:5, flexWrap:"wrap" }}>
                    <span style={{ fontSize:8, padding:"1px 4px", background:t.badge, color:"#fff", letterSpacing:1 }}>
                      {s.type==="daytime"?"DAY":"NIGHT"}
                    </span>
                    <span style={{ fontSize:8, color:"#3a3a3a" }}>{uDot[s.urg]} {s.urg.toUpperCase()}</span>
                    <span style={{ fontSize:8, color:"#222" }}>km{s.km} · {s.dist}km</span>
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
                      <S l="POPULATION" c={t.accent} t={s.swing}/>
                      <S l="RESIDENTIAL" c={t.accent}>{s.res.map((r,i)=><L key={i}>{r}</L>)}</S>
                      <S l="WORK" c={t.accent}>{s.work.map((w,i)=><L key={i}>{w}</L>)}</S>
                    </div>
                    <div>
                      <S l="NIGHT ANGLE" c={t.accent} t={s.night}/>
                      <S l="ROUTE" c={t.accent}>
                        <div style={{ fontSize:10, color:"#fff", fontWeight:500 }}>{s.route}</div>
                        <div style={{ fontSize:8, color:"#333", marginTop:1 }}>{s.dist}km</div>
                      </S>
                      <div style={{ padding:7, marginTop:4, background:"#030303", border:`1px solid ${t.border}15` }}>
                        <div style={{ fontSize:7, color:t.accent, letterSpacing:2, marginBottom:2 }}>WHY</div>
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
          <div style={{ display:"grid", gridTemplateColumns:"repeat(5,1fr)", gap:10 }}>
            {[
              [stats.day,"#FF9800","Daytime"],
              [stats.night,"#7986CB","Nocturnal"],
              [stats.crit,"#ef5350","Critical"],
              [stats.high,"#FFA726","High"],
              ["~12k","#fff","Night workers stranded"]
            ].map(([n,c,d],i)=>(
              <div key={i}>
                <div style={{ fontSize:16, color:c, fontWeight:300 }}>{n}</div>
                <div style={{ fontSize:8, color:"#444" }}>{d}</div>
              </div>
            ))}
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
