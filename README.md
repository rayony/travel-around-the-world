# Travel around the world

Closed great-circle tour of **196 places** (Hong Kong + 195 national capitals): start in Hong Kong, visit each capital **exactly once**, return to Hong Kong, minimise the sum of spherical distances.

This is a metric **Travelling Salesman Problem** on the sphere. Exact dynamic programming (Held–Karp) is impossible at n = 196. The maps show **heuristics**, not a proven global optimum.

Interactive lesson + map: open [`docs/hk_capital_tour_map.html`](docs/hk_capital_tour_map.html) in a browser (needs network for Leaflet, OpenStreetMap tiles, and the NASA image).

## Repository layout

| Path | What |
| --- | --- |
| `data/capitals_0-195.csv` | Cleaned CityID 0–195, names, lat/lng, PosX/PosY |
| `solvers/tsp_capitals.py` | Haversine + NN / multi-start NN / farthest insertion / 2-opt / Or-opt / 3-opt |
| `docs/hk_capital_tour_map.html` | Map player + step-by-step algorithm lesson |
| `output/` | Optional JSON from the solver |

The original workbook was `trial 0 - blind.xlsm`. The CSV is the corrected 0–195 table used for every kilometre figure.

## How the length is measured

Earth is treated as a sphere of radius **6371.0088 km**. Distance is the haversine great-circle formula. A 196×196 matrix is built once; every algorithm only looks up that table.

PosX / PosY are `round(100 × longitude)` and `round(100 × latitude)` and are **not** used for length.

## Algorithms that were actually run

All tours below are valid Hamiltonian cycles (each CityID once, start and end = Hong Kong).

| Method | About | Length (km) |
| --- | --- | --- |
| Nearest neighbour from HK only | Greedy next-closest unvisited city | 173,672 |
| Multi-start NN (196 seeds), rotate cut to HK | Same greedy, best seed, then rotate | 171,305 |
| Farthest insertion | Insert the city farthest from the current tour at the cheapest edge | 154,728 |
| Farthest insertion + 2-opt | | 153,600 |
| 2-opt on multi-start NN | Reverse a segment when two edges get shorter | 149,529 |
| Simulated annealing in the 2-opt neighbourhood | No extra 2-opt gain from the 2-opt tour | 149,529 |
| **2-opt + Or-opt + 2-opt** | Relocate a chain of 1–3 cities | **147,945** |
| 3-opt after Or-opt (valid cycles only) | No shorter legal 3-opt found | 147,945 |

An earlier 3-opt figure of ~147,484 km **reused cities** and was discarded.

Held–Karp, Lin–Kernighan / LKH, and Concorde are explained in the HTML lesson but were **not** executed here.

```bash
python3 solvers/tsp_capitals.py --data data/capitals_0-195.csv --out output/tours.json
```

Requires Python 3.9+. No third-party packages.

## Basemap licensing (why Esri is not used)

The viewer **does not** call Esri / ArcGIS Online tile services (`server.arcgisonline.com`, World Street Map, World Imagery).

Those endpoints fall under the Esri Master License Agreement. Esri documents that live World Imagery / street tiles are not a free anonymous API: they expect an ArcGIS Online or ArcGIS Location Platform account, “Powered by Esri” plus data-vendor attribution, and they are not licensed as a drop-in public basemap for an unauthenticated GitHub page. That is why they were removed.

Instead:

1. **OpenStreetMap raster tiles** — `https://tile.openstreetmap.org/{z}/{x}/{y}.png`  
   Data © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright).  
   Follow the [OSM tile policy](https://operations.osmfoundation.org/policies/tiles/) (reasonable traffic, attribution, no bulk scraping).

2. **NASA Blue Marble Next Generation** (December, topography + bathymetry), loaded **from NASA**, not stored in this repo:

   - Credit page: [NASA Visible Earth — December Blue Marble: Next Generation w/ Topography and Bathymetry](https://visibleearth.nasa.gov/images/73909/december-blue-marble-next-generation-w-topography-and-bathymetry)
   - Direct JPEG used by the HTML: https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg
   - Credit: NASA Earth Observatory / NASA Visible Earth (US federal government work; keep the credit).

If OSM tiles fail, the page falls back to that NASA image.

## Licence for this repo’s own files

Solver, HTML lesson, and cleaned table: [MIT](LICENSE).
OpenStreetMap data and NASA imagery remain under their own terms.
