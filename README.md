# Travel around the world

Closed great-circle tour of **196 places** (Hong Kong + 195 UN member/observer capitals): start in Hong Kong, visit each capital **exactly once**, return to Hong Kong, minimise the sum of spherical distances.

## Open the map

The interactive player and algorithm lesson is a single file:

[`docs/hk_capital_tour_map.html`](docs/hk_capital_tour_map.html)

Open it in a desktop browser (needs network for Leaflet + the NASA JPEG). GitHub’s file preview will **not** run the map; use raw / local file / GitHub Pages.

Default basemap is **NASA Blue Marble** on `EPSG:4326` so city pins sit on the same equirectangular grid as the image (Hong Kong should fall on the east side of the Pearl River estuary). Optional layer: OSM WMS in the same CRS. Do not paste the NASA image onto Web Mercator — latitude will drift.

On-map credit is short (`NASA Blue Marble (EPSG:4326)`). Full credit is in the Leaflet attribution and below.

## Assumption: UN membership list as of 2026-09-14

This project **follows the United Nations list of Member States and Non-Member Observer States**, snapshot date **14 September 2026**.

- https://www.un.org/en/about-us/member-states
- https://www.un.org/en/about-us/non-member-states

| Rule | What we do |
| --- | --- |
| Set of states | **193 members** (last new member: South Sudan, 14 July 2011) + **2 observers** (Holy See; State of Palestine since 29 November 2012) = **195** rows |
| Not on the UN pages | No Taiwan / Taipei, no Kosovo, no Western Sahara, no Macao, no other ISO territories |
| Extra 196th point | Hong Kong (CityID 0) is only the tour start/end. Nation cell `-`. Not a UN state |
| Names aligned 2026-09-14 | Cabo Verde, Czechia, Türkiye, Congo, Timor-Leste, State of Palestine, Holy See, Côte D'Ivoire |
| Capitals | Unchanged (Israel = Jerusalem, State of Palestine = Ramallah) |
| Not used | Full ISO 3166; any one country’s diplomatic recognition list |

Heuristic TSP only. Held–Karp is impossible at n = 196.

## Repository layout

| Path | What |
| --- | --- |
| `docs/hk_capital_tour_map.html` | Map + lesson (upload / replace this file when the viewer changes) |
| `data/capitals_0-195.csv` | Cleaned CityID 0–195 |
| `data/SOURCES.md` | Imagery credits |
| `solvers/tsp_capitals.py` | Haversine + NN / farthest insertion / 2-opt / Or-opt / 3-opt |

Original workbook: `trial 0 - blind.xlsm`.

## Distance

Sphere radius **6371.0088 km**, haversine, 196×196 lookup table. PosX / PosY = `round(100 × lon/lat)` and are not used for length.

## Algorithms that were run (valid Hamiltonian cycles only)

| Method | km |
| --- | ---: |
| Nearest neighbour from HK | 173,672 |
| Multi-start NN, rotate cut to HK | 171,305 |
| Farthest insertion | 154,728 |
| Farthest insertion + 2-opt | 153,600 |
| 2-opt on multi-start NN | 149,529 |
| Simulated annealing (2-opt neighbourhood) | 149,529 |
| **2-opt + Or-opt + 2-opt** | **147,945** |
| 3-opt after Or-opt (legal cycles only) | 147,945 |

A shorter ~147,484 km 3-opt reused cities and was discarded. Held–Karp, Lin–Kernighan / LKH, and Concorde are taught in the HTML but were not executed.

```bash
python3 solvers/tsp_capitals.py --data data/capitals_0-195.csv --out output/tours.json
```

Python 3.9+, no third-party packages.

## Basemap licensing

**No Esri / ArcGIS Online tiles.** Those services need an Esri licence and prescribed attribution; they are not used.

- Default: NASA Blue Marble Next Generation (December, topography + bathymetry), loaded from NASA, not stored in the repo.  
  Item: https://visibleearth.nasa.gov/images/73909/december-blue-marble-next-generation-w-topography-and-bathymetry  
  JPEG: https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg  
  Credit: NASA Earth Observatory / NASA Visible Earth.
- Optional: OSM as WMS in EPSG:4326 (© OpenStreetMap contributors, ODbL; renderer terrestris).

## Licence

Code and cleaned table: [MIT](LICENSE). OSM data and NASA imagery stay under their own terms.
