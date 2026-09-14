# Travel around the world

Closed great-circle tour of **196 places** (Hong Kong + 195 UN member/observer capitals): start in Hong Kong, visit each capital **exactly once**, return to Hong Kong, minimise the sum of spherical distances.

## Assumption: UN membership list as of 2026-09-14

This project **follows the United Nations list of Member States and Non-Member Observer States**, snapshot date **14 September 2026**.

Sources still published on that date:

- https://www.un.org/en/about-us/member-states
- https://www.un.org/en/about-us/non-member-states

| Rule | What we do |
| --- | --- |
| Set of states | **193 members** (last new member: South Sudan, 14 July 2011) + **2 observers** (Holy See; State of Palestine since 29 November 2012) = **195** rows |
| Not on the UN pages | No Taiwan / Taipei, no Kosovo, no Western Sahara, no Macao, no other ISO territories |
| Extra 196th point | Hong Kong (CityID 0) is only the tour start/end. The nation cell is `-`. It is not treated as a UN state |
| Names aligned 2026-09-14 | Cabo Verde, Czechia, Türkiye, Congo, Timor-Leste, State of Palestine, Holy See, Côte D'Ivoire |
| Capitals | Unchanged (Israel = Jerusalem, Palestine = Ramallah). UN pages list states, not a capital gazetteer |
| Not used | ISO 3166 complete list; any one country’s diplomatic recognition list |

This is a metric **Travelling Salesman Problem** on the sphere. Exact Held–Karp is impossible at n = 196. The maps show **heuristics**, not a proven global optimum.

Interactive lesson + map: open [`docs/hk_capital_tour_map.html`](docs/hk_capital_tour_map.html) in a browser (needs network for Leaflet, OpenStreetMap tiles, and the NASA image).

## Repository layout

| Path | What |
| --- | --- |
| `data/capitals_0-195.csv` | Cleaned CityID 0–195, UN-aligned names, lat/lng, PosX/PosY |
| `solvers/tsp_capitals.py` | Haversine + NN / multi-start NN / farthest insertion / 2-opt / Or-opt / 3-opt |
| `docs/hk_capital_tour_map.html` | Map player + step-by-step algorithm lesson |
| `output/` | Optional JSON from the solver |

The original workbook was `trial 0 - blind.xlsm`.

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

The viewer **does not** call Esri / ArcGIS Online tile services.

Instead:

1. **OpenStreetMap raster tiles** — `https://tile.openstreetmap.org/{z}/{x}/{y}.png` © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright).
2. **NASA Blue Marble Next Generation**, loaded from NASA, not stored in this repo: [Visible Earth item 73909](https://visibleearth.nasa.gov/images/73909/december-blue-marble-next-generation-w-topography-and-bathymetry) — https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg — credit NASA Earth Observatory / NASA Visible Earth.

## Licence for this repo’s own files

Solver, HTML lesson, and cleaned table: [MIT](LICENSE).
