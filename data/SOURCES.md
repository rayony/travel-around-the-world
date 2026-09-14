# Data and imagery sources

## Capitals table

`capitals_0-195.csv` is a cleaned copy of the original `trial 0 - blind.xlsm` (CityID 0 = Hong Kong, then 195 UN-oriented states). Coordinates that were wrong in the source workbook were corrected before any tour length was computed.

## NASA Blue Marble (static world image)

Not stored in this repository. The HTML viewer requests NASA’s file directly.

- Item page (credit this): https://visibleearth.nasa.gov/images/73909/december-blue-marble-next-generation-w-topography-and-bathymetry
- Direct JPEG: https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg
- Credit line: NASA Earth Observatory / NASA Visible Earth, *Blue Marble: Next Generation* (December, topography and bathymetry).

## OpenStreetMap tiles

https://tile.openstreetmap.org/{z}/{x}/{y}.png  
© OpenStreetMap contributors, ODbL. Tile usage: https://operations.osmfoundation.org/policies/tiles/

## Esri / ArcGIS Online

**Not used.** World Street Map and World Imagery on `services.arcgisonline.com` / `server.arcgisonline.com` require an Esri licence (ArcGIS Online or Location Platform) and prescribed attribution. They are not included as a default or fallback in this project.
