// ============================================================
// City101 Interactive Maps — Shared Module
// Leaflet-based interactive maps for the Archipelago narrative
// ============================================================

const City101Maps = (() => {

  // === CACHE ===
  let _contextCache = null;
  let _extraDataCache = {};

  // === TILE LAYER ===
  function darkTiles() {
    return L.tileLayer(
      'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
      {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
        subdomains: 'abcd',
        maxZoom: 18,
        opacity: 0.85
      }
    );
  }

  // === BOUNDS PRESETS ===
  const BOUNDS = {
    FULL_CORRIDOR: [[46.15, 6.05], [46.56, 7.02]],
    LAVAUX_ZOOM:   [[46.44, 6.66], [46.53, 6.90]],
    GENEVA_ZOOM:   [[46.16, 6.06], [46.29, 6.22]],
    LAUSANNE_ZOOM: [[46.49, 6.53], [46.56, 6.70]],
  };

  // === COLOR SCALES ===
  function wciColor(wci) {
    // Red → Yellow → Green gradient (0 → 0.3 → 0.65+)
    if (wci <= 0.02) return '#6b1a1a';
    if (wci <= 0.05) return '#b33a3a';
    if (wci <= 0.10) return '#e74c3c';
    if (wci <= 0.15) return '#e67e22';
    if (wci <= 0.25) return '#f1c40f';
    if (wci <= 0.40) return '#2ecc71';
    return '#27ae60';
  }

  function wciRadius(wci) {
    if (wci <= 0.02) return 5;
    if (wci <= 0.05) return 6;
    if (wci <= 0.10) return 7;
    if (wci <= 0.20) return 8;
    if (wci <= 0.40) return 10;
    return 13;
  }

  function freqColor(freq) {
    if (freq <= 0) return '#6b1a1a';
    if (freq <= 2) return '#b33a3a';
    if (freq <= 4) return '#e74c3c';
    if (freq <= 6) return '#e67e22';
    if (freq <= 10) return '#f1c40f';
    if (freq <= 16) return '#2ecc71';
    return '#27ae60';
  }

  function freqRadius(freq) {
    if (freq <= 2) return 5;
    if (freq <= 4) return 6;
    if (freq <= 8) return 8;
    if (freq <= 16) return 10;
    return 13;
  }

  const SEG_COLORS = {
    'Geneva': '#e74c3c',
    'La Côte': '#e67e22',
    'Lausanne': '#3498db',
    'Lavaux': '#9b59b6',
    'Riviera': '#2ecc71'
  };

  const WORK_COLORS = {
    'coworking': '#e74c3c',
    'café': '#1abc9c',
    'library': '#3498db'
  };

  // === POPUP BUILDERS ===
  function stationPopup(s) {
    const seg = `<span style="color:${SEG_COLORS[s.segment] || '#8a8880'}">${s.segment}</span>`;
    return `
      <strong>${s.name}</strong><br>
      ${seg} · ${s.rail_km} km from Geneva<br>
      <span style="color:${wciColor(s.wci)}">● WCI: ${s.wci.toFixed(3)}</span><br>
      Frequency: ${s.freq} trains/hr<br>
      Richness: ${s.richness} amenities<br>
      Shannon: ${s.shannon.toFixed(2)}<br>
      Service: ${s.service_hrs}h/day
    `;
  }

  function workspacePopup(w) {
    const color = WORK_COLORS[w.type] || '#8a8880';
    return `
      <strong>${w.name}</strong><br>
      <span style="color:${color}">● ${w.type}</span><br>
      ${w.rating ? `★ ${w.rating}` : ''}
    `;
  }

  function evPopup(p) {
    return `
      <strong>${p.name || 'EV Station'}</strong><br>
      <span style="color:#2ecc71">● EV Charging</span><br>
      ${p.power_kw ? `Power: ${p.power_kw} kW` : ''}
      ${p.connectors ? `<br>Connectors: ${p.connectors}` : ''}
      ${p.operator ? `<br>Operator: ${p.operator}` : ''}
      ${p.is_24h === 'yes' ? '<br>24h access' : ''}
    `;
  }

  function wifiPopup(p) {
    return `
      <strong>${p.name || 'WiFi Hotspot'}</strong><br>
      <span style="color:#3498db">● WiFi</span><br>
      ${p.location_type ? `Type: ${p.location_type.replace(/_/g, ' ')}` : ''}
      ${p.quality_score ? `<br>Quality: ${p.quality_score}/5` : ''}
      ${p.hours ? `<br>Hours: ${p.hours}` : ''}
    `;
  }

  function mobilityPopup(p) {
    return `
      <strong>${p.name || 'Shared Mobility'}</strong><br>
      <span style="color:#e67e22">● Shared Mobility</span><br>
      ${p.provider ? `Provider: ${p.provider}` : ''}
      ${p.vehicle_types ? `<br>Vehicles: ${p.vehicle_types}` : ''}
    `;
  }

  function lateNightPopup(v) {
    const typeColors = { bar: '#e67e22', cafe: '#1abc9c', nightclub: '#9b59b6', food_shop_24h: '#f1c40f' };
    const color = typeColors[v.type] || '#8a8880';
    return `
      <strong>${v.name}</strong><br>
      <span style="color:${color}">● ${v.type}</span><br>
      ${v.seg || ''}
    `;
  }

  // === LAYER FACTORIES ===

  function createWCILayer(stations, options = {}) {
    const group = L.layerGroup();
    stations.forEach(s => {
      const marker = L.circleMarker([s.lat, s.lon], {
        radius: wciRadius(s.wci),
        fillColor: wciColor(s.wci),
        color: 'rgba(255,255,255,0.3)',
        weight: 1,
        opacity: 1,
        fillOpacity: 0.85
      }).bindPopup(stationPopup(s));

      // Add station label for major stations
      if (options.showLabels && s.wci > 0.1) {
        const label = L.tooltip({
          permanent: true,
          direction: 'right',
          offset: [10, 0],
          className: 'station-label'
        }).setContent(s.name);
        marker.bindTooltip(label);
      }
      group.addLayer(marker);
    });
    return group;
  }

  function createRemoteWorkLayer(data) {
    const group = L.layerGroup();
    data.forEach(w => {
      const color = WORK_COLORS[w.type] || '#8a8880';
      L.circleMarker([w.lat, w.lon], {
        radius: 6,
        fillColor: color,
        color: 'rgba(255,255,255,0.2)',
        weight: 1,
        fillOpacity: 0.8
      }).bindPopup(workspacePopup(w)).addTo(group);
    });
    return group;
  }

  function createTransitFreqLayer(stations) {
    const group = L.layerGroup();
    stations.forEach(s => {
      L.circleMarker([s.lat, s.lon], {
        radius: freqRadius(s.freq),
        fillColor: freqColor(s.freq),
        color: 'rgba(255,255,255,0.3)',
        weight: 1,
        fillOpacity: 0.85
      }).bindPopup(`
        <strong>${s.name}</strong><br>
        <span style="color:${freqColor(s.freq)}">● ${s.freq} trains/hr</span><br>
        Service: ${s.service_hrs}h/day<br>
        ${s.segment}
      `).addTo(group);
    });
    return group;
  }

  function createGeoJSONLayer(geojson, options) {
    return L.geoJSON(geojson, {
      pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
          radius: options.radius || 5,
          fillColor: options.color || '#8a8880',
          color: 'rgba(255,255,255,0.15)',
          weight: 1,
          fillOpacity: options.opacity || 0.7
        });
      },
      onEachFeature: (feature, layer) => {
        if (options.popup) {
          layer.bindPopup(options.popup(feature.properties));
        }
      }
    });
  }

  function createLateNightLayer(data) {
    const typeColors = { bar: '#e67e22', cafe: '#1abc9c', nightclub: '#9b59b6', food_shop_24h: '#f1c40f' };
    const group = L.layerGroup();
    data.forEach(v => {
      L.circleMarker([v.lat, v.lon], {
        radius: 5,
        fillColor: typeColors[v.type] || '#8a8880',
        color: 'rgba(255,255,255,0.15)',
        weight: 1,
        fillOpacity: 0.75
      }).bindPopup(lateNightPopup(v)).addTo(group);
    });
    return group;
  }

  // === CONTEXT LAYERS ===

  async function fetchJSON(url) {
    try {
      const res = await fetch(url);
      return res.json();
    } catch (e) {
      console.warn(`fetch failed for ${url}, using inline data`);
      return null;
    }
  }

  async function loadContextLayers(map) {
    if (!_contextCache) {
      // Use inline GEODATA_* globals (from city101_geodata.js) if available,
      // otherwise fall back to fetch (works on http:// servers)
      const lake = (typeof GEODATA_LAKE !== 'undefined' ? GEODATA_LAKE : null)
                   || await fetchJSON('data/lake_leman.geojson');
      const trains = (typeof GEODATA_TRAINS !== 'undefined' ? GEODATA_TRAINS : null)
                     || await fetchJSON('data/train_lines.geojson');
      const communes = (typeof GEODATA_COMMUNES !== 'undefined' ? GEODATA_COMMUNES : null)
                       || await fetchJSON('data/communes.geojson');
      _contextCache = { lake, trains, communes };
    }

    // Communes — very subtle borders
    if (_contextCache.communes) {
      L.geoJSON(_contextCache.communes, {
        style: {
          fillColor: 'transparent',
          color: 'rgba(255,255,255,0.06)',
          weight: 0.5
        }
      }).addTo(map);
    }

    // Lake — dark blue
    if (_contextCache.lake) {
      L.geoJSON(_contextCache.lake, {
        style: {
          fillColor: '#0c0f1e',
          fillOpacity: 0.6,
          color: 'rgba(255,255,255,0.08)',
          weight: 1
        }
      }).addTo(map);
    }

    // Train lines — gold accent
    if (_contextCache.trains) {
      L.geoJSON(_contextCache.trains, {
        style: {
          color: '#c8a86e',
          weight: 1.5,
          opacity: 0.6
        }
      }).addTo(map);
    }
  }

  // === EXTRA DATA LOADERS ===

  async function loadExtraData(type) {
    if (_extraDataCache[type]) return _extraDataCache[type];

    // Use inline GEODATA_* globals first (from city101_geodata.js)
    const inlineData = {
      ev: typeof GEODATA_EV !== 'undefined' ? GEODATA_EV : null,
      wifi: typeof GEODATA_WIFI !== 'undefined' ? GEODATA_WIFI : null,
      mobility: typeof GEODATA_MOBILITY !== 'undefined' ? GEODATA_MOBILITY : null,
    };

    if (inlineData[type]) {
      _extraDataCache[type] = inlineData[type];
      return inlineData[type];
    }

    // Fallback: fetch from GeoJSON files (works on http:// servers)
    const urls = {
      ev: 'data/ev_charging.geojson',
      wifi: 'data/wifi_hotspots.geojson',
      mobility: 'data/shared_mobility.geojson'
    };

    if (!urls[type]) return null;
    const data = await fetchJSON(urls[type]);
    if (data) _extraDataCache[type] = data;
    return data;
  }

  // === LEGEND BUILDERS ===

  function createWCILegend() {
    const div = L.DomUtil.create('div', 'map-legend');
    div.innerHTML = `
      <div class="legend-title">WCI Score</div>
      <div class="legend-item"><span class="legend-dot" style="background:#27ae60"></span> 0.40+</div>
      <div class="legend-item"><span class="legend-dot" style="background:#2ecc71"></span> 0.25–0.40</div>
      <div class="legend-item"><span class="legend-dot" style="background:#f1c40f"></span> 0.15–0.25</div>
      <div class="legend-item"><span class="legend-dot" style="background:#e67e22"></span> 0.10–0.15</div>
      <div class="legend-item"><span class="legend-dot" style="background:#e74c3c"></span> 0.05–0.10</div>
      <div class="legend-item"><span class="legend-dot" style="background:#b33a3a"></span> 0.02–0.05</div>
      <div class="legend-item"><span class="legend-dot" style="background:#6b1a1a"></span> < 0.02</div>
    `;
    return div;
  }

  function createFreqLegend() {
    const div = L.DomUtil.create('div', 'map-legend');
    div.innerHTML = `
      <div class="legend-title">Trains/Hour</div>
      <div class="legend-item"><span class="legend-dot" style="background:#27ae60"></span> 16+</div>
      <div class="legend-item"><span class="legend-dot" style="background:#2ecc71"></span> 10–16</div>
      <div class="legend-item"><span class="legend-dot" style="background:#f1c40f"></span> 6–10</div>
      <div class="legend-item"><span class="legend-dot" style="background:#e67e22"></span> 4–6</div>
      <div class="legend-item"><span class="legend-dot" style="background:#e74c3c"></span> 2–4</div>
      <div class="legend-item"><span class="legend-dot" style="background:#b33a3a"></span> 0–2</div>
    `;
    return div;
  }

  function createWorkLegend() {
    const div = L.DomUtil.create('div', 'map-legend');
    div.innerHTML = `
      <div class="legend-title">Remote Work</div>
      <div class="legend-item"><span class="legend-dot" style="background:#e74c3c"></span> Coworking</div>
      <div class="legend-item"><span class="legend-dot" style="background:#1abc9c"></span> Café</div>
      <div class="legend-item"><span class="legend-dot" style="background:#3498db"></span> Library</div>
    `;
    return div;
  }

  // === MAP INITIALIZER ===

  async function init(containerId, config) {
    const container = document.getElementById(containerId);
    if (!container) return null;

    const bounds = config.bounds || BOUNDS.FULL_CORRIDOR;

    const map = L.map(containerId, {
      zoomControl: true,
      scrollWheelZoom: true,
      attributionControl: true,
      minZoom: 10,
      maxZoom: 18
    });

    darkTiles().addTo(map);
    map.fitBounds(bounds, { padding: [20, 20] });

    // Load context layers
    await loadContextLayers(map);

    // Add data layers based on config
    const overlays = {};

    if (config.layers) {
      for (const layerConfig of config.layers) {
        let layer;

        switch (layerConfig.type) {
          case 'wci':
            layer = createWCILayer(
              typeof STATIONS !== 'undefined' ? STATIONS : [],
              { showLabels: layerConfig.showLabels }
            );
            break;

          case 'remote_work':
            layer = createRemoteWorkLayer(
              typeof REMOTE_WORK !== 'undefined' ? REMOTE_WORK : []
            );
            break;

          case 'transit_freq':
            layer = createTransitFreqLayer(
              typeof STATIONS !== 'undefined' ? STATIONS : []
            );
            break;

          case 'late_night':
            layer = createLateNightLayer(
              typeof LATE_NIGHT !== 'undefined' ? LATE_NIGHT : []
            );
            break;

          case 'ev': {
            const evData = await loadExtraData('ev');
            if (evData) {
              layer = createGeoJSONLayer(evData, {
                radius: 5,
                color: '#2ecc71',
                opacity: 0.75,
                popup: evPopup
              });
            }
            break;
          }

          case 'wifi': {
            const wifiData = await loadExtraData('wifi');
            if (wifiData) {
              layer = createGeoJSONLayer(wifiData, {
                radius: 4,
                color: '#3498db',
                opacity: 0.7,
                popup: wifiPopup
              });
            }
            break;
          }

          case 'mobility': {
            const mobData = await loadExtraData('mobility');
            if (mobData) {
              layer = createGeoJSONLayer(mobData, {
                radius: 3,
                color: '#e67e22',
                opacity: 0.4,
                popup: mobilityPopup
              });
            }
            break;
          }
        }

        if (layer) {
          const name = layerConfig.name || layerConfig.type;
          overlays[name] = layer;

          if (layerConfig.visible !== false) {
            layer.addTo(map);
          }
        }
      }
    }

    // Add layer control if there are multiple overlays
    if (Object.keys(overlays).length > 1 || config.showLayerControl) {
      L.control.layers(null, overlays, {
        collapsed: true,
        position: 'topright'
      }).addTo(map);
    }

    // Add legend
    if (config.legend) {
      const legend = L.control({ position: 'bottomright' });
      legend.onAdd = () => {
        switch (config.legend) {
          case 'wci': return createWCILegend();
          case 'freq': return createFreqLegend();
          case 'work': return createWorkLegend();
          default: return L.DomUtil.create('div');
        }
      };
      legend.addTo(map);
    }

    return map;
  }

  // === PUBLIC API ===
  return {
    init,
    BOUNDS,
    wciColor,
    freqColor,
    SEG_COLORS,
    WORK_COLORS,
    createWCILayer,
    createRemoteWorkLayer,
    createTransitFreqLayer,
    createLateNightLayer,
    loadContextLayers,
    loadExtraData
  };

})();
