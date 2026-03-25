# Data Inventory — City101 Source Files

**Generated:** 2026-02-28  
**Total files:** 233  

## File Type Summary

| Type | Count |
|------|------:|
| CSV | 104 |
| GeoPackage | 53 |
| PDF | 30 |
| GeoJSON | 17 |
| QGIS Project | 8 |
| Python Script | 4 |
| GPX | 4 |
| XML Metadata | 4 |
| GeoTIFF Raster | 3 |
| Markdown | 2 |
| PNG Image | 2 |
| Grid Raster | 1 |
| Unknown/Custom format | 1 |

---

## 00-datasets 2

### CSV Files

| File | Rows | Columns |
|------|-----:|---------|
| `alexeipotapushin-coop.csv` | 73 | ﻿chain, store_name, address, lat_wgs84, lon_wgs84, E_LV95, N_LV95, rating, rating_count |
| `alexeipotapushin-tierA.csv` | 13 | node_id, name, tier, tier_label, category, subcategory, operator, annual_packages_k, transport_modes, address, postal... |
| `alexeipotapushin-tierB.csv` | 21 | node_id, name, tier, tier_label, category, subcategory, operator, annual_packages_k, transport_modes, address, postal... |
| `alexeipotapushin-tierC.csv` | 13 | node_id, name, tier, tier_label, category, subcategory, operator, annual_packages_k, transport_modes, address, postal... |
| `andreacrespo-EV charging Reviews.csv` | 109 | station_name, municipality, operator, google_place_id, station_rating, review_text, tags, sentiment |
| `andreacrespo-EV charging.csv` | 194 | id, name, operator, network, connectors, capacity, access, vehicle_type, address, municipality, latitude_wgs84, longi... |
| `andreacrespo-cell_towers.csv` | 3218 | tower_id, operator, technology, has_3g, has_4g, has_5g, power_class, station_type, is_indoor, E_lv95, N_lv95, lat_wgs... |
| `andreacrespo-international_anchors.csv` | 15 | anchor_id, short_id, name, lat_wgs84, lon_wgs84, E_lv95, N_lv95, location_type, category, scale, connectivity_cluster |
| `andreacrespo-remote_work_REVIEWS.csv` | 109 | place_name, municipality, place_type, google_place_id, review_text, tags, is_work_relevant, sentiment |
| `andreacrespo-remote_work_places.csv` | 68 | name, latitude_wgs84, longitude_wgs84, place_type, google_rating, google_review_count, address, municipality, google_... |
| `andreacrespo-wifi.csv` | 81 | station_id, name, lat_wgs84, lon_wgs84, E_lv95, N_lv95, location_type, wifi_category, wifi_quality_score, operator_ne... |
| `dejeancharlene-gigwork.csv` | 50 | id, municipality, place_name, work_type, platform, workers_est, season, permit_status, latitude, longitude, dist_lake... |
| `dejeancharlene-rooftops.csv` | 27 | id, building_name, city, address, latitude, longitude, coordinate_source, building_type, floors_approx, roof_area_m2_... |
| `electronics_repair.csv` | 24 | Latitude, Longitude, Name, Address, City, Rating, Service_Type, Place_ID |
| `ewaste_collection.csv` | 13 | Latitude, Longitude, Name, Address, City, Rating, Facility_Type, Place_ID |
| `new_electronics_stores.csv` | 20 | Latitude, Longitude, Name, Address, City, Rating, Phone_Type, Place_ID |
| `secondhand_electronics.csv` | 18 | Latitude, Longitude, Name, Address, City, Rating, Store_Type, Place_ID |
| `dimitriroulet-hazardouswaste.csv` | 6 | Nom, Filiere, Sous_type, Commune, Canton, Adresse, Exploitant, Latitude, Longitude, Statut, Notes, Coords_Status |
| `dimitriroulet-incinairationsite.csv` | 3 | Nom, Filiere, Sous_type, Commune, Canton, Adresse, Exploitant, Latitude, Longitude, Statut, Notes, Coords_Status |
| `dimitriroulet-industrialcomposting.csv` | 8 | Nom, Type, Commune, Canton, Adresse, Latitude, Longitude, Capacité_Production, Notes, Coords_Status |
| `dimitriroulet-inertlandfill.csv` | 10 | Nom, Type_OLED, Commune, Canton, Adresse, Exploitant, Latitude, Longitude, Statut, Notes, Coords_Status |
| `dimitriroulet-wastecollectioncentre.csv` | 30 | Nom, Type, Commune, Canton, Adresse, Latitude, Longitude, Horaires, Téléphone, Notes, Communes_desservies |
| `dimitriroulet-wastesorting.csv` | 11 | Nom, Type, Opérateur, Commune, Canton, Adresse, Latitude, Longitude, Téléphone, Notes, Coords_Status |
| `dimitriroulet-wastewater.csv` | 41 | type_infrastructure, nom, adresse, commune, canton, latitude, longitude, capacite_eq_hab, verification, source, notes |
| `hennarafik-UHIhighpeakheatislands.csv` | 40 | zone_name, latitude_wgs84, longitude_wgs84, E_LV95, N_LV95, UHI_category, UHI_intensity_score, description, land_use_... |
| `hennarafik-UHIlowcoolzones.csv` | 109 | zone_name, latitude_wgs84, longitude_wgs84, E_LV95, N_LV95, UHI_category, UHI_intensity_score, description, land_use_... |
| `hennarafik-UHImediumtransitionzones.csv` | 54 | zone_name, latitude_wgs84, longitude_wgs84, E_LV95, N_LV95, UHI_category, UHI_intensity_score, description, land_use_... |
| `hennarafik-coldairdrainage.csv` | 50 | name, E_LV95, N_LV95, elevation_m, flow_role, type, capacity_or_blockage, flow_direction, description |
| `hennarafik-localtraditions.csv` | 119 | name, category, subcategory, description, season, frequency, latitude_wgs84, longitude_wgs84, E_lv95, N_lv95, urban_z... |
| `hennarafik-rotatingculturalcircuits.csv` | 43 | circuit_name, circuit_type, federation, year, host_location, latitude, longitude, corridor_segment, estimated_partici... |
| `hennarafik-stationridership.csv` | 22 | station_name, daily_avg_passengers, workday_avg_passengers, km_along_corridor, latitude_wgs84, longitude_wgs84, E_lv9... |
| `hennarafik-thermalcomfort.csv` | 33 | name, E_LV95, N_LV95, actual_UHI_zone, perceived_comfort, shade_condition, water_proximity, wind_exposure, surface_al... |
| `all_shops_complete.csv` | 30 | name, place_type, category, canton, lat_wgs84, lon_wgs84, E_LV95, N_LV95, osm_node_id |
| `building_materials.csv` | 3 | name, place_type, canton, lat_wgs84, lon_wgs84, E_LV95, N_LV95, osm_node_id |
| `clothing_shops.csv` | 16 | name, place_type, canton, lat_wgs84, lon_wgs84, E_LV95, N_LV95, osm_node_id |
| `furniture_accessories.csv` | 11 | name, place_type, canton, lat_wgs84, lon_wgs84, E_LV95, N_LV95, osm_node_id |
| `STEP_NorthShore_LakeGeneva_complete.csv` | 9 | plant_name, city, canton, capacity_population_equivalent, water_body_recipient, E_LV95, N_LV95, notes |
| `lake_geneva_north_shore_villages.csv` | 27 | name, place_type, canton, lat_wgs84, lon_wgs84, E_LV95, N_LV95, osm_node_id |
| `juliefavre-apple-farms.csv` | 47 | id, name, type, municipality, canton, address, lat_wgs84, lon_wgs84, lv95_e, lv95_n, source, notes |
| `juliefavre-commercial-hubs.csv` | 47 | id, name, hub_type, sub_type, municipality, canton, address, lat_wgs84, lon_wgs84, lv95_e, lv95_n, frequency, source,... |
| `juliefavre-pollinatorhubs.csv` | 29 | Hub ID, Pollinator Hub Name, Municipality, Classification, Habitat Type, Latitude, Longitude, LV95 East, LV95 North, ... |
| `cipel_2024_donnees_brutes.csv` | 44 | Station, X_CH1903, Y_CH1903, Lon, Lat, Date, Profondeur_m, Temp_C, pH, O2_sat_pct, Secchi_m, Ptot_ugP_L, PO4_ugP_L, N... |
| `leman_flux_microbiens_cipel_2024.csv` | 59 | Station, Nom_Station, X_CH1903, Y_CH1903, Longitude, Latitude, Zone_Lac, Profondeur_Max_m, Annee, Mois, Parametre, Va... |
| `leman_macrophytes_moules_2019.csv` | 42 | Secteur, Type_Donnee, Annee, Profondeur_Min_m, Profondeur_Max_m, Distance_Berge_m, Espece_Dominante, Recouvrement_Pct... |
| `leman_qualite_eau_coordonnees_corrigees2.csv` | 39 | Station_Mesure, Coordonnee_X_Suisse, Coordonnee_Y_Suisse, Longitude, Latitude, Date_Campagne, Profondeur_Eau_m, Tempe... |
| `step_arc_lemanique_complet_corrige.csv` | 26 | Numero_Station, Nom_Station, Coordonnee_X_Suisse, Coordonnee_Y_Suisse, Altitude_m, Adresse_Complete, Code_Postal, Com... |
| `step_arc_lemanique_traduit.csv` | 16 | Numero_Station, Nom_Station, Coordonnee_X_Suisse, Coordonnee_Y_Suisse, Altitude_m, Adresse_Complete, Code_Postal, Com... |
| `step_wgs84.csv` | 26 | Numero_Station, Nom_Station, Coordonnee_X_Suisse, Coordonnee_Y_Suisse, Altitude_m, Adresse_Complete, Code_Postal, Com... |
| `magasins_aldi.csv` | 9 | ﻿Enseigne, Nom, Adresse, Commune, NPA, Canton, Latitude, Longitude |
| `magasins_coop.csv` | 44 | ﻿Enseigne, Nom, Adresse, Commune, NPA, Canton, Latitude, Longitude |
| `magasins_denner.csv` | 30 | ﻿Enseigne, Nom, Adresse, Commune, NPA, Canton, Latitude, Longitude |
| `magasins_lidl.csv` | 10 | ﻿Enseigne, Nom, Adresse, Commune, NPA, Canton, Latitude, Longitude |
| `magasins_migros.csv` | 28 | ﻿Enseigne, Nom, Adresse, Commune, NPA, Canton, Latitude, Longitude |
| `magasins_supermarches.csv` | 121 | ﻿Enseigne, Nom, Adresse, Commune, NPA, Canton, Latitude, Longitude |
| `All_ecoles_public_arc_lemanique.csv` | 199 | ﻿ID, Nom, Type, Commune, Canton, Region, Adresse, Latitude_WGS84, Longitude_WGS84, E_LV95, N_LV95, Source, Statut_Coo... |
| `ecoles_primaires.csv` | 90 | ﻿ID, Nom, Type, Commune, Canton, Region, Adresse, Latitude_WGS84, Longitude_WGS84, E_LV95, N_LV95, Source, Statut_Coo... |
| `ecoles_primaires_secondaires.csv` | 49 | ﻿ID, Nom, Type, Commune, Canton, Region, Adresse, Latitude_WGS84, Longitude_WGS84, E_LV95, N_LV95, Source, Statut_Coo... |
| `ecoles_secondaires.csv` | 32 | ﻿ID, Nom, Type, Commune, Canton, Region, Adresse, Latitude_WGS84, Longitude_WGS84, E_LV95, N_LV95, Source, Statut_Coo... |
| `gymnases_colleges.csv` | 28 | ﻿ID, Nom, Type, Commune, Canton, Region, Adresse, Latitude_WGS84, Longitude_WGS84, E_LV95, N_LV95, Source, Statut_Coo... |
| `A01_food_systems_restaurants.csv` | 150 | name, type, cuisine, chain, latitude, longitude, municipality, source |
| `A01_knowledge_flows_informal_learning.csv` | 132 | name, type, public_or_private, access_type, latitude, longitude, municipality, source |
| `noebrun-Churches.csv` | 42 | nom, adresse, E_LV95, N_LV95 |
| `noebrun-Ephemeral events.csv` | 49 | nom, adresse, E_LV95, N_LV95 |
| `noebrun-ports.csv` | 48 | nom, type, commune, canton, E_LV95, N_LV95 |
| `simeonpavicevic-energyconsumption.csv` | 20 | id, nom, type_consommateur, conso_elec_GWh_an, conso_therm_GWh_an, population_emplois, commune, canton, LV95_E, LV95_... |
| `simeonpavicevic-energyproduction.csv` | 20 | id, nom, type_source, technologie, production_elec_GWh_an, production_therm_GWh_an, puissance_MW, exploitant, commune... |
| `simeonpavicevic-industrialsectors.csv` | 195 | NOM_ENTREPRISE, COMMUNE, ADRESSE, LONGITUDE, LATITUDE, E_LV95, N_LV95, CODE_NOGA, SECTEUR, ETP, INTENSITE_ENERGETIQUE... |
| `simeonpavicevic-industrialzones.csv` | 25 | ID, Nom_zone, Acronyme, Canton, Commune_s, District, E_LV95, N_LV95, Lat_WGS84, Lon_WGS84, Surface_ha, Nb_entreprises... |
| `stellaguicciardi-birdhouse.csv` | 473 | id, source_dataset, name_fr, city, categorie_type, categorie_label, espece, lat_wgs84, lon_wgs84, east_lv95, north_lv... |
| `stellaguicciardi-birdhousegeneve.csv` | 55 | id, nom, adresse, commune, canton, categorie_type, categorie_label, type_infrastructure, especes_cibles, nb_nichoirs,... |
| `stellaguicciardi-lausannebirds.csv` | 377 | east_lv95, north_lv95, espece, art_nest, nat_nest, p_nat_nest, localisati, detail_loc, remarques, categorie_type, cat... |
| `stellaguicciardi-temporarystructure.csv` | 100 | structure_id, structure_name, structure_type, city, location_description, lat_wgs84, lon_wgs84, east_lv95, north_lv95... |
| `thomasriegert-budhistcommunities.csv` | 11 | nom, adresse, tradition, E_LV95, N_LV95 |
| `thomasriegert-budhisttemples.csv` | 25 | nom, adresse, latitude_wgs84, longitude_wgs84, coord_E_lv95, coord_N_lv95, type, ville |
| `thomasriegert-christianbuildings.csv` | 134 | nom, adresse, ville, type, coord_e_lv95, coord_n_lv95, latitude_wgs84, longitude_wgs84 |
| `thomasriegert-christiancommunities.csv` | 59 | nom, commune, canton, type, unite_pastorale, adresse, E_LV95, N_LV95 |
| `thomasriegert-esotericism.csv` | 43 | nom, adresse, latitude_wgs84, longitude_wgs84, coord_E_lv95, coord_N_lv95, type, sous_type, ville |
| `thomasriegert-evangelicalcommunities.csv` | 68 | nom, commune, canton, denomination, federation, adresse, E_LV95, N_LV95 |
| `thomasriegert-generalpractitioners.csv` | 112 | Nom, Adresse, Ville, Code_Postal, LV95_E, LV95_N, Latitude, Longitude, Note, Nb_Avis |
| `thomasriegert-hinducommunities.csv` | 8 | nom, adresse, tradition, E_LV95, N_LV95 |
| `thomasriegert-hindutemples.csv` | 4 | nom, adresse, latitude_wgs84, longitude_wgs84, coord_E_lv95, coord_N_lv95, type, ville |
| `thomasriegert-jewishbuildings.csv` | 7 | nom, adresse, courant, statut, E_LV95, N_LV95 |
| `thomasriegert-jewishcommunities.csv` | 10 | nom, commune, canton, courant, organisation, adresse, E_LV95, N_LV95 |
| `thomasriegert-muslimbuildings.csv` | 24 | nom, adresse, latitude_wgs84, longitude_wgs84, coord_E_lv95, coord_N_lv95, type, ville |
| `thomasriegert-muslimcommunities.csv` | 37 | nom, commune, canton, type, courant, adresse, E_LV95, N_LV95 |
| `thomasriegert-orthodoxbuildings.csv` | 15 | nom, adresse, tradition, E_LV95, N_LV95 |
| `thomasriegert-orthodoxcommunities.csv` | 15 | nom, adresse, tradition, E_LV95, N_LV95 |
| `thomasriegert-otherreligiousbuildings.csv` | 4 | nom, adresse, latitude_wgs84, longitude_wgs84, coord_E_lv95, coord_N_lv95, type, ville |
| `thomasriegert-privateclinics.csv` | 68 | nom, adresse, ville, coord_e_lv95, coord_n_lv95, latitude_wgs84, longitude_wgs84 |
| `thomasriegert-protestantbuildings.csv` | 12 | nom, adresse, latitude_wgs84, longitude_wgs84, coord_E_lv95, coord_N_lv95, type, ville |
| `thomasriegert-protestantcommunities.csv` | 54 | nom, commune, canton, type, region_ecclesiastique, adresse, E_LV95, N_LV95 |
| `thomasriegert-publichospitals.csv` | 23 | Nom, Type, Adresse, Ville, Note_Google, Latitude_WGS84, Longitude_WGS84, E_LV95, N_LV95 |
| `thomasriegert-specialists.csv` | 188 | Nom, Adresse, Spécialité, Latitude_WGS84, Longitude_WGS84, LV95_E, LV95_N, Note |
| `vladislavbelov-acousticecology..csv` | 50 | id, name, category, subcategory, location_name, municipality, lat_WGS84, lon_WGS84, osm_verified, noise_level_dBA, te... |
| `vladislavbelov-localmaterials..csv` | 38 | name, type, material_category, location, municipality, latitude, longitude, aquatic, description, source, verificatio... |

### GeoJSON Files

| File | Features | Geometry | Properties |
|------|--------:|----------|------------|
| `alexeipotapushin-addedmanuallyvector.geojson` | 6 | LineString | DIST_KM, DURATION_H, PROFILE, PREF, OPTIONS, FROM_ID, TO_ID, layer, path |
| `alexeipotapushin-fullroutes.geojson` | 83 | LineString | connection_no, from_id, from_name, to_id, to_name, route_type, ors_profile, direction, est_dist_k... |
| `alexeipotapushin-migros.geojson` | 73 | LineString | from_chain, from_name, from_rating, to_chain, to_name, to_rating, distance_m, distance_km, rating... |
| `juliefavre-flows-farm-to-markets.geojson` | 60 | LineString | flow_id, farm_id, farm_name, market_id, market_name, flow_type, farm_type, distance_km, supply_po... |
| `lhiamrossier-bas-marais.geojson` | 14 | MultiPolygon | fid, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Inkraftset, Mutationsd, Mutationsg, SHA... |
| `lhiamrossier-carte-aptitude-sols.geojson` | 241 | MultiPolygon | fid, ID_OBJET, Surface, Perimetre, BEK200, BEK200_ID, Code_interne, Code, Couleur, Longueur, Code... |
| `lhiamrossier-corridors-microbiens.geojson` | 91 | Point | fid, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Inkraftset, Mutationsd, Mutationsg, SHA... |
| `lhiamrossier-degrade-qualite-lac.geojson` | None | E, x, p, e, c, t, i, n, g,  , v, a, l, u, e, :,  , l, i, n, e,  , 1,  , c, o, l, u, m, n,  , 1,  , (, c, h, a, r,  , 0, ) | — |
| `lhiamrossier-lac-leman.geojson` | 1 | Polygon | fid |
| `lhiamrossier-morphologie-chutes.geojson` | 1190 | Point | fid, ID_OBJET, Num_CE_2007, Mesure_2007, OID_OM, Num_CE_OM, Mesure_OM, Statut_OM, Premiere_saisie... |
| `lhiamrossier-morphologie-troncons.geojson` | 2216 | MultiLineString | fid, ID_OBJET, Num_CE_2007, De_2007, A_2007, Num_troncon_OM, Num_CE_OM, Mesure_debut_OM, Mesure_f... |
| `lhiamrossier-qualite-eaux-cipel.geojson` | None | E, x, p, e, c, t, i, n, g,  , v, a, l, u, e, :,  , l, i, n, e,  , 1,  , c, o, l, u, m, n,  , 1,  , (, c, h, a, r,  , 0, ) | — |
| `lhiamrossier-step-performance.geojson` | None | E, x, p, e, c, t, i, n, g,  , v, a, l, u, e, :,  , l, i, n, e,  , 1,  , c, o, l, u, m, n,  , 1,  , (, c, h, a, r,  , 0, ) | — |
| `lhiamrossier-zones-alluviales.geojson` | 12 | MultiPolygon | fid, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Typ, Inkraftset, Mutationsd, Mutationsg... |
| `lhiamrossier-zones-influence-step.geojson` | None | E, x, p, e, c, t, i, n, g,  , v, a, l, u, e, :,  , l, i, n, e,  , 1,  , c, o, l, u, m, n,  , 1,  , (, c, h, a, r,  , 0, ) | — |
| `lhiamrossier-zones-reproduction-amphibiens.geojson` | 65 | MultiPolygon | fid, ID_OBJET, Num_objet, Nom, Fiche_reference, Type_designation, Categorie_UICN, Date_mise_vigue... |
| `simeonpavicevic-energyflows.geojson` | 46 | LineString | id_flux, source_id, source_nom, destination_id, destination_nom, type_flux, energie_dominante, fl... |

### GeoPackage Files

**`andreacrespo-CellTowers.gpkg`** (664.0 KB)

- Layer **City101_CellTowers** — POINT, 3218 rows  
  Columns: fid, geom, tower_id, operator, technology, has_5g, has_4g, has_3g, power_class, station_type, is_indoor

**`andreacrespo-InternationalAnchors.gpkg`** (96.0 KB)

- Layer **City101_InternationalAnchors** — POINT, 15 rows  
  Columns: fid, geom, anchor_id, short_id, name, location_type, category, scale, connectivity_cluster

**`andreacrespo-Public_WiFi_81.gpkg`** (112.0 KB)

- Layer **Public_WiFi_81** — POINT, 81 rows  
  Columns: fid, geom, station_id, name, location_type, wifi_category, wifi_quality_score, operator_network, indoor_outdoor, hour...

**`hennarafik-ColdAirDrainage.gpkg`** (104.0 KB)

- Layer **FLOW_01_ColdAirDrainage_LINES_v2** — LINESTRING, 22 rows  
  Columns: fid, geom, name, flow_strength, obstruction, elev_source_m, elev_sink_m, elev_drop_m

**`hennarafik-PsychoComfort.gpkg`** (104.0 KB)

- Layer **FLOW_10_PsychoComfort_LINES** — LINESTRING, 15 rows  
  Columns: fid, geom, name, line_type, comfort_quality, description

**`hennarafik-flowmeaningspine.gpkg`** (104.0 KB)

- Layer **flow_meaningspine** — LINESTRING, 40 rows  
  Columns: fid, geom, from_station, to_station, avg_passengers, meaning_avg, segment_type

**`hennarafik-flowrotatingcircuits.gpkg`** (104.0 KB)

- Layer **flow2_rotatingcircuits_v03** — POINT, 43 rows  
  Columns: fid, geom, circuit_name, circuit_type, federation, year, host_location, latitude, longitude, corridor_segment, estima...

**`hennarafik-flowtransitstops.gpkg`** (104.0 KB)

- Layer **flow_transitstops** — POINT, 77 rows  
  Columns: fid, geom, name, type, daily_passengers, traditions_nearby, km_corridor

**`190226_TLM3D_City101_v3_EN.gpkg`** (748.0 MB)

- Layer **road_junction** — POINT, 153 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **land_cover** — MULTIPOLYGON, 34465 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **individual_tree_shrub** — POINT, 802264 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **individual_object** — POINT, 1880 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **building_footprint** — MULTIPOLYGON, 313960 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **road_info** — POINT, 145768 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **supply_infrastructure** — POINT, 625 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **land_use_area** — MULTIPOLYGON, 3896 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **wall** — MULTILINESTRING, 538 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **dam_structure** — MULTIPOLYGON, 12882 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **stabilisation_structure** — MULTILINESTRING, 4258 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **traffic_area** — MULTIPOLYGON, 1816 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **leisure_area** — MULTIPOLYGON, 362 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **sport_structure_lin** — MULTILINESTRING, 158 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **sport_structure_ply** — MULTIPOLYGON, 2035 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **transport_structure_lin** — MULTILINESTRING, 291 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **transport_structure_ply** — MULTIPOLYGON, 342 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **transit_stop** — POINT, 3033 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **locality_name** — MULTIPOLYGON, 3821 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **place_name** — POINT, 10160 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **named_point** — POINT, 402 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **road** — MULTILINESTRING, 184600 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **watercourse** — MULTILINESTRING, 26381 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **standing_water** — MULTILINESTRING, 2192 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_MONAT, ERSTELLUNG_JAHR, REVISION_JAHR, REVIS...
- Layer **waterway_navigation** — MULTILINESTRING, 0 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **railway** — MULTILINESTRING, 5672 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **other_railway** — MULTILINESTRING, 147 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **power_line** — MULTILINESTRING, 148 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, GRUND_AENDERUNG, HER...
- Layer **region_name** — MULTIPOLYGON, 198 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **terrain_name** — MULTIPOLYGON, 331 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...
- Layer **protected_area** — MULTIPOLYGON, 0 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`190226_TLM3D_City101_v3_FR.gpkg`** (754.5 MB)

- Layer **entree_sortie** — POINT, 153 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **couverture_sol** — MULTIPOLYGON, 34465 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **arbre_individuel_buisson** — POINT, 802264 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **objet_individuel** — POINT, 1880 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **emprise_batiment** — MULTIPOLYGON, 313960 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **info_route** — POINT, 145768 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **infrastructure_approvisionnement** — POINT, 625 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **zone_utilisation** — MULTIPOLYGON, 3896 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **mur** — MULTILINESTRING, 538 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **ouvrage_retenue** — MULTIPOLYGON, 12882 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **ouvrage_stabilisation** — MULTILINESTRING, 4258 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **zone_trafic** — MULTIPOLYGON, 1816 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **zone_de_loisirs** — MULTIPOLYGON, 362 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **infrastructure_sport_lin** — MULTILINESTRING, 158 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **infrastructure_sport_ply** — MULTIPOLYGON, 2035 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **infrastructure_transport_lin** — MULTILINESTRING, 291 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **infrastructure_transport_ply** — MULTIPOLYGON, 342 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **arret_transport** — POINT, 3033 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **nom_localite** — MULTIPOLYGON, 3821 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **lieu_dit** — POINT, 10160 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **nom_point** — POINT, 402 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **route** — MULTILINESTRING, 184600 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **cours_deau** — MULTILINESTRING, 26381 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **eaux_stagnantes** — MULTILINESTRING, 2192 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, MOIS_CREATION, ANNEE_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **navigation** — MULTILINESTRING, 0 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **chemin_de_fer** — MULTILINESTRING, 5672 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **autre_voie_ferree** — MULTILINESTRING, 147 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **ligne_electrique** — MULTILINESTRING, 148 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, MOTIF_MODIFICATION, ORIGI...
- Layer **nom_region** — MULTIPOLYGON, 198 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **nom_terrain** — MULTIPOLYGON, 331 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **zone_protegee** — MULTIPOLYGON, 0 rows  
  Columns: fid, geom, ID_OBJET, UUID, DATE_MODIFICATION, DATE_CREATION, ANNEE_CREATION, MOIS_CREATION, ANNEE_REVISION, MOIS_REVI...
- Layer **ruissellement_surface** — MULTIPOLYGON, 2473 rows  
  Columns: fid, geom, CODE_GRILLE, CLASSE_PENTE, DATE_CREATION, ID_ORIGINE, LONGUEUR, SUPERFICIE

**`lhiamrossier-bas-marais.gpkg`** (984.0 KB)

- Layer **lhiamrossier-bas-marais** — MULTIPOLYGON, 14 rows  
  Columns: fid, geom, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Inkraftset, Mutationsd, Mutationsg, SHAPE_Leng, SHAPE...

**`lhiamrossier-carte-aptitude-sols.gpkg`** (812.0 KB)

- Layer **lhiamrossier-carte-aptitude-sols** — MULTIPOLYGON, 241 rows  
  Columns: fid, geom, ID_OBJET, Surface, Perimetre, BEK200, BEK200_ID, Code_interne, Code, Couleur, Longueur, Code_KU, Aptitude,...

**`lhiamrossier-corridors-microbiens.gpkg`** (176.0 KB)

- Layer **lhiamrossier-corridors-microbiens** — POINT, 91 rows  
  Columns: fid, geom, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Inkraftset, Mutationsd, Mutationsg, SHAPE_Leng, SHAPE...

**`lhiamrossier-degrade-qualite-lac.gpkg`** (560.0 KB)

- Layer **lhiamrossier-degrade-qualite-lac** — POLYGON, 5 rows  
  Columns: fid, geom, zone, couleur

**`lhiamrossier-lac-leman.gpkg`** (492.0 KB)

- Layer **lhiamrossier-lac-leman** — POLYGON, 1 rows  
  Columns: fid, geom

**`lhiamrossier-morphologie-chutes.gpkg`** (464.0 KB)

- Layer **lhiamrossier-morphologie-chutes** — POINT, 1190 rows  
  Columns: fid, geom, ID_OBJET, Num_CE_2007, Mesure_2007, OID_OM, Num_CE_OM, Mesure_OM, Statut_OM, Premiere_saisie, Source_donne...

**`lhiamrossier-morphologie-troncons.gpkg`** (1.9 MB)

- Layer **lhiamrossier-morphologie-troncons** — MULTILINESTRING, 2216 rows  
  Columns: fid, geom, ID_OBJET, Num_CE_2007, De_2007, A_2007, Num_troncon_OM, Num_CE_OM, Mesure_debut_OM, Mesure_fin_OM, Statut_...

**`lhiamrossier-qualite-eaux-cipel.gpkg`** (96.0 KB)

- Layer **lhiamrossier-qualite-eaux-cipel** — POINT, 7 rows  
  Columns: fid, geom, nom, phosphore, brettum, qualite, transparence

**`lhiamrossier-step-performance.gpkg`** (104.0 KB)

- Layer **lhiamrossier-step-performance** — POINT, 26 rows  
  Columns: fid, geom, nom, commune, capacite, capacite_label, population, taux_charge, categorie_perf, raison, couleur, traiteme...

**`lhiamrossier-water-microbes.gpkg`** (5.3 MB)

- Layer **carte-aptitude-sols** — MULTIPOLYGON, 241 rows  
  Columns: fid, geom, ID_OBJET, Surface, Perimetre, BEK200, BEK200_ID, Code_interne, Code, Couleur, Longueur, Code_KU, Aptitude,...
- Layer **lac-leman** — POLYGON, 1 rows  
  Columns: fid, geom
- Layer **morphologie-chutes** — POINT, 1190 rows  
  Columns: fid, geom, ID_OBJET, Num_CE_2007, Mesure_2007, OID_OM, Num_CE_OM, Mesure_OM, Statut_OM, Premiere_saisie, Source_donne...
- Layer **morphologie-troncons** — MULTILINESTRING, 2216 rows  
  Columns: fid, geom, ID_OBJET, Num_CE_2007, De_2007, A_2007, Num_troncon_OM, Num_CE_OM, Mesure_debut_OM, Mesure_fin_OM, Statut_...
- Layer **zones-reproduction-amphibiens** — MULTIPOLYGON, 65 rows  
  Columns: fid, geom, ID_OBJET, Num_objet, Nom, Fiche_reference, Type_designation, Categorie_UICN, Date_mise_vigueur, Date_mutat...
- Layer **corridors-microbiens** — POINT, 91 rows  
  Columns: fid, geom, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Inkraftset, Mutationsd, Mutationsg, SHAPE_Leng, SHAPE...
- Layer **zones-alluviales** — MULTIPOLYGON, 12 rows  
  Columns: fid, geom, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Typ, Inkraftset, Mutationsd, Mutationsg, Shape_Leng, ...
- Layer **bas-marais** — MULTIPOLYGON, 14 rows  
  Columns: fid, geom, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Inkraftset, Mutationsd, Mutationsg, SHAPE_Leng, SHAPE...

**`lhiamrossier-waterquality.gpkg`** (736.0 KB)

- Layer **step_performance** — POINT, 26 rows  
  Columns: fid, geom, nom, commune, capacite, capacite_label, population, taux_charge, categorie_perf, raison, couleur, traiteme...
- Layer **qualite_eaux_cipel** — POINT, 7 rows  
  Columns: fid, geom, nom, phosphore, brettum, qualite, transparence
- Layer **zones_influence_step** — MULTIPOLYGON, 26 rows  
  Columns: fid, geom, nom, commune, capacite, capacite_label, population, taux_charge, categorie_perf, raison, couleur, traiteme...
- Layer **degrade_qualite_lac** — POLYGON, 5 rows  
  Columns: fid, geom, zone, couleur

**`lhiamrossier-zones-alluviales.gpkg`** (168.0 KB)

- Layer **lhiamrossier-zones-alluviales** — MULTIPOLYGON, 12 rows  
  Columns: fid, geom, ObjNummer, Name, RefObjBlat, DesignatTy, IUCNCatego, Typ, Inkraftset, Mutationsd, Mutationsg, Shape_Leng, ...

**`lhiamrossier-zones-influence-step.gpkg`** (200.0 KB)

- Layer **lhiamrossier-zones-influence-step** — MULTIPOLYGON, 26 rows  
  Columns: fid, geom, nom, commune, capacite, capacite_label, population, taux_charge, categorie_perf, raison, couleur, traiteme...

**`lhiamrossier-zones-reproduction-amphibiens.gpkg`** (336.0 KB)

- Layer **lhiamrossier-zones-reproduction-amphibiens** — MULTIPOLYGON, 65 rows  
  Columns: fid, geom, ID_OBJET, Num_objet, Nom, Fiche_reference, Type_designation, Categorie_UICN, Date_mise_vigueur, Date_mutat...

**`Local Materials.gpkg`** (116.0 KB)

- Layer **city101_localmaterials3** — POINT, 28 rows  
  Columns: fid, geom, name, type, material_category, location, municipality, latitude, longitude, aquatic, description, source, ...

**`Local materials selected.gpkg`** (120.0 KB)

- Layer **city101_localmaterials3** — POINT, 38 rows  
  Columns: fid, geom, name, type, material_category, location, municipality, latitude, longitude, aquatic, description, source, ...

**`Map Polygon.gpkg`** (104.0 KB)

- Layer **map_polygon** — POLYGON, 3 rows  
  Columns: fid, geom

### GPX Files

| File | Waypoints | Tracks | Routes | Track Points |
|------|----------:|-------:|-------:|-------------:|
| `aimericmarin-library.gpx` | 54 | 0 | 0 | 0 |
| `aimericmarin-museum.gpx` | 65 | 0 | 0 | 0 |
| `aimericmarin-sailboatspath_ports.gpx` | 0 | 2415 | 0 | 626502 |
| `aimericmarin-theater.gpx` | 64 | 0 | 0 | 0 |

### Other Files

| File | Type | Size | Notes |
|------|------|------|-------|
| `aimericmarin-cultural_spaces.png` | PNG Image | 2.4 MB |  |
| `aimericmarin-sailboats.png` | PNG Image | 4.8 MB |  |
| `alexeipotapushin-ecommerce.pdf` | PDF | 11.7 MB |  |
| `alexeipotapushin-migroscoop.pdf` | PDF | 10.6 MB |  |
| `andreacrespo-Charging Infrastructure as the New Spin...-Bike Networks Along the Arc Lémanique.pdf` | PDF | 287.5 KB |  |
| `andreacrespo-Dashboard_EV_DataArchitecture.pdf` | PDF | 45.1 KB |  |
| `andreacrespo-Dashboard_EV_Operators.pdf` | PDF | 43.0 KB |  |
| `andreacrespo-Dashboard_EV_Overview.pdf` | PDF | 42.5 KB |  |
| `andreacrespo-enrich_ocm.py` | Python Script | 14.0 KB | 369 lines |
| `andreacrespo-_Program_of_Stopping_vf.pdf` | PDF | 8.7 MB |  |
| `andreacrespo-Dashboard_RemoteWork_Gaps.pdf` | PDF | 59.1 KB |  |
| `andreacrespo-Dashboard_RemoteWork_Overview.pdf` | PDF | 43.9 KB |  |
| `andreacrespo-Where_Can_You_Work_vf.pdf` | PDF | 4.5 MB |  |
| `andreacrespo-enrich_wifi_v3.py` | Python Script | 17.4 KB | 488 lines |
| `andreacrespo-public wifi remote work infrastructure.md` | Markdown | 30.6 KB | 243 lines |
| `andreacrespo-Charging stations and invisible flows.qgz` | QGIS Project | 177.8 KB |  |
| `cristinamartinez-intergenerational-exange.xxx` | Unknown/Custom format | 148.0 KB |  |
| `cristinamartinez-results.pdf` | PDF | 22.4 MB |  |
| `cristinamartinez-social-segregation.xxx.qgz` | QGIS Project | 174.5 KB |  |
| `W1 appareil elec.pdf` | PDF | 2.1 MB |  |
| `w1 garage.pdf` | PDF | 2.8 MB |  |
| `hennarafik-coolairdrainage.pdf` | PDF | 23.0 MB |  |
| `hennarafik-flowofmeaning-transitstops.pdf` | PDF | 19.6 MB |  |
| `hennarafik-flowofmeaning.pdf` | PDF | 19.6 MB |  |
| `hennarafik-geopsychocomfort-1-15000.pdf` | PDF | 22.9 MB |  |
| `hennarafik-geopsychocomfort-2-25000.pdf` | PDF | 15.4 MB |  |
| `hennarafik-localtraditions.pdf` | PDF | 20.0 MB |  |
| `hennarafik-localtraditions.qgz` | QGIS Project | 165.3 KB |  |
| `hennarafik-localtraditionsheritage.pdf` | PDF | 19.8 MB |  |
| `hennarafik-urbanheatislands.pdf` | PDF | 24.1 MB |  |
| `hennarafik-urbanheatislands.qgz` | QGIS Project | 165.6 KB |  |
| `juliefavre-farm-flows.pdf` | PDF | 7.8 MB |  |
| `juliefavre-pollinator-flows.pdf` | PDF | 952.8 KB |  |
| `Map Food.pdf` | PDF | 1.8 MB |  |
| `Map Public School.pdf` | PDF | 1.2 MB |  |
| `CITY101_Foodsystems_InformalLearning.qgz` | QGIS Project | 149.8 KB |  |
| `A01_FoodSystems.pdf` | PDF | 7.2 MB |  |
| `A01_InformalLearning.pdf` | PDF | 7.3 MB |  |
| `thomasriegert-heatlh&spiritualflow.qgz` | QGIS Project | 192.7 KB |  |
| `vladislavbelov-acousticecology..pdf` | PDF | 921.2 KB |  |
| `vladislavbelov-acousticecology..qgz` | QGIS Project | 178.0 KB |  |
| `vladislavbelov-localmaterials..qgz` | QGIS Project | 171.4 KB |  |
| `vladislavbelov-localmaterials.pdf` | PDF | 9.0 MB |  |
| `Daylight Railway Noise.tif` | GeoTIFF Raster | 40.9 MB |  |
| `Daylight Railway Noise.tif.aux.xml` | XML Metadata | 1.5 KB |  |
| `Daylight Road Traffic noise raster.tif` | GeoTIFF Raster | 72.7 MB |  |
| `Daylight Road Traffic noise raster.tif.aux.xml` | XML Metadata | 1.5 KB |  |
| `Export tranquility.grd.aux.xml` | XML Metadata | 1.1 KB |  |
| `Export tranquility.gri` | Grid Raster | 27.1 MB |  |
| `Tranquility Raster.tif` | GeoTIFF Raster | 26.2 MB |  |
| `Tranquility Raster.tif.aux.xml` | XML Metadata | 1.5 KB |  |

## 00-datasets 3

### Other Files

| File | Type | Size | Notes |
|------|------|------|-------|
| `stellaguicciardi-mapsbirdhouses+temporarystructure.pdf` | PDF | 53.2 MB |  |

## Charging station csv copy

### CSV Files

| File | Rows | Columns |
|------|-----:|---------|
| `city101_ev_charging_ENRICHED_v3.csv` | 194 | id, name, operator, network, connectors, capacity, access, vehicle_type, address, municipality, latitude_wgs84, longi... |
| `city101_ev_charging_REVIEWS.csv` | 109 | station_name, municipality, operator, google_place_id, station_rating, review_text, tags, sentiment |

### Other Files

| File | Type | Size | Notes |
|------|------|------|-------|
| `enrich_ocm.py` | Python Script | 14.0 KB | 369 lines |

## Documents copy

### GeoPackage Files

**`City101_GroundCover.gpkg`** (26.8 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_bodenbedeckung_CITY101** — MULTIPOLYGON, 11332 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_LeisureArea.gpkg`** (544.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_freizeitareal_CITY101** — MULTIPOLYGON, 268 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_SmallBuildings.gpkg`** (5.1 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_staubaute_CITY101** — MULTIPOLYGON, 10747 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

## WORK copy

### GeoPackage Files

**`City101_Buildings.gpkg`** (144.8 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_gebaeude_footprint_CITY101** — MULTIPOLYGON, 218437 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_CantonalBoundaries.gpkg`** (532.0 KB)

- Layer **swissboundaries3d_1_5_lv95_ln02__tlm_kantonsgebiet_CITY101** — MULTIPOLYGON, 2 rows  
  Columns: fid, geom, OBJECTID, Shape_Length, Shape_Area, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_M...

**`City101_Communes.gpkg`** (1.4 MB)

- Layer **swissboundaries3d_1_5_lv95_ln02__tlm_communes_CITY101** — MULTILINESTRING, 493 rows  
  Columns: fid, geom, OBJECTID, Shape_Length, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, GRUND_...

**`City101_Communes_SURFACE.gpkg`** (1.9 MB)

- Layer **swissboundaries3d_1_5_lv95_ln02__tlm_CommunesPOLY** — MULTIPOLYGON, 150 rows  
  Columns: fid, geom, OBJECTID, Shape_Length, Shape_Area, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_M...

**`City101_FieldNames.gpkg`** (1.2 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_flurname_City101** — POINT, 3944 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_Flowing_Waters.gpkg`** (9.3 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_fliessgewaesser_CITY101** — MULTILINESTRING, 8698 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_GroundCover.gpkg`** (180.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_sportbaute_lin_CITY101** — MULTILINESTRING, 95 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_Highway_EntryExits.gpkg`** (144.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_aus_einfahrt_CITY101** — POINT, 132 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_LakeLeman.gpkg`** (492.0 KB)

- Layer **City101_LakeLeman** — POLYGON, 1 rows  
  Columns: fid, geometry

**`City101_PeakNames.gpkg`** (124.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_name_pkt_CITY101** — POINT, 53 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_Road_NODES.gpkg`** (23.5 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_strasseninfo_City101** — POINT, 102837 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_SingleTreesBush.gpkg`** (95.7 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_einzelbaum_gebuesch_CITY101** — POINT, 451591 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_SpecialUse_Area.gpkg`** (4.5 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_nutzungsareal_CITY101** — MULTIPOLYGON, 3034 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_Sports_Fields.gpkg`** (820.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_sportbaute_ply_CITY101** — MULTIPOLYGON, 1706 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_StandingWater.gpkg`** (1.6 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_stehendes_gewaesser_CITY101** — MULTILINESTRING, 1118 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_MONAT, ERSTELLUNG_JAHR, REVISION_JAHR, REVIS...

**`City101_Streets.gpkg`** (66.0 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_strasse_CITY101** — MULTILINESTRING, 132054 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_TrafficZonesParkings.gpkg`** (1.2 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_verkehrsareal_CITY101** — MULTIPOLYGON, 1379 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_Traffic_Structures.gpkg`** (188.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_verkehrsbaute_lin_CITY101** — MULTILINESTRING, 221 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_TrainLines.gpkg`** (30.0 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_eisenbahn_CITY101** — MULTILINESTRING, 4044 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_Transit_Buildings_AirportETC.gpkg`** (312.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_verkehrsbaute_ply_City101** — MULTIPOLYGON, 209 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_Transit_Stops.gpkg`** (732.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_haltestelle_CITY101** — POINT, 2207 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_VillageNames.gpkg`** (5.9 MB)

- Layer **swisstlm3d_chlv95ln02__tlm_siedlungsname_CITY101** — MULTIPOLYGON, 2484 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

**`City101_Walls.gpkg`** (176.0 KB)

- Layer **swisstlm3d_chlv95ln02__tlm_mauer_CITY101** — MULTILINESTRING, 163 rows  
  Columns: fid, geom, OBJECTID, UUID, DATUM_AENDERUNG, DATUM_ERSTELLUNG, ERSTELLUNG_JAHR, ERSTELLUNG_MONAT, REVISION_JAHR, REVIS...

## invisible flows copy

### CSV Files

| File | Rows | Columns |
|------|-----:|---------|
| `city101_cell_towers.csv` | 3218 | tower_id, operator, technology, has_3g, has_4g, has_5g, power_class, station_type, is_indoor, E_lv95, N_lv95, lat_wgs... |
| `city101_international_anchors.csv` | 15 | anchor_id, short_id, name, lat_wgs84, lon_wgs84, E_lv95, N_lv95, location_type, category, scale, connectivity_cluster |
| `city101_remote_work_REVIEWS.csv` | 109 | place_name, municipality, place_type, google_place_id, review_text, tags, is_work_relevant, sentiment |
| `city101_remote_work_places.csv` | 68 | name, latitude_wgs84, longitude_wgs84, place_type, google_rating, google_review_count, address, municipality, google_... |
| `city101_wifi_MERGED.csv` | 56 | station_id, name, lat_wgs84, lon_wgs84, E_lv95, N_lv95, location_type, wifi_category, wifi_quality_score, operator_ne... |
| `city101_wifi_MERGEDv.2.csv` | 81 | station_id, name, lat_wgs84, lon_wgs84, E_lv95, N_lv95, location_type, wifi_category, wifi_quality_score, operator_ne... |
| `city101_wifi_MERGEDv3.csv` | 81 | station_id, name, lat_wgs84, lon_wgs84, E_lv95, N_lv95, location_type, wifi_category, wifi_quality_score, operator_ne... |

### Other Files

| File | Type | Size | Notes |
|------|------|------|-------|
| `enrich_wifi_v3.py` | Python Script | 17.4 KB | 488 lines |
| `public wifi remote work infrastructure.md` | Markdown | 30.6 KB | 243 lines |
