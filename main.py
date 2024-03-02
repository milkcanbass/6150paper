import gtfs_kit as gk
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Load GTFS data
gtfs_path = '/Users/shintarokai/Dev/Paper/Data/TTC Routes and Schedules Data.zip'  # Update this with the path to your GTFS dataset
feed = gk.read_feed(gtfs_path, dist_units='km')

# Search for a specific route by its short name
route_short_name = "1"  # Make sure this is a string
specific_route = feed.routes[feed.routes['route_short_name'] == route_short_name]

if not specific_route.empty:
    trips = feed.trips[feed.trips.route_id.isin(specific_route.route_id)]
    stop_times = feed.stop_times[feed.stop_times.trip_id.isin(trips.trip_id)]
    stops = stop_times.merge(feed.stops, on='stop_id')
    gdf_stops = gpd.GeoDataFrame(stops, geometry=gpd.points_from_xy(stops.stop_lon, stops.stop_lat), crs='EPSG:4326')
    gdf_stops = gdf_stops.to_crs(epsg=3857)

    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_stops.plot(ax=ax, color='blue', markersize=5, alpha=0.6, label='Stops')

    # Check if 'shapes' attribute exists in the feed
    if hasattr(feed, 'shapes'):
        shapes = feed.shapes[feed.shapes.shape_id.isin(trips.shape_id)]
        gdf_shapes = gpd.GeoDataFrame(shapes, geometry=gpd.points_from_xy(shapes.shape_pt_lon, shapes.shape_pt_lat), crs='EPSG:4326')
        gdf_shapes = gdf_shapes.to_crs(epsg=3857)
        gdf_shapes.plot(ax=ax, color='red', linewidth=2, label='Route Path')

    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_axis_off()
    plt.legend()
    plt.show()

else:
    print("No route found with the short name:", route_short_name)