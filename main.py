
import pandas as pd
import requests
import json
import geopandas as gpd
from geodatasets import get_path


# setup values to loop through the API requests
raw_list = []

# Fetching data from the API
for i in range(0, 10):
    r = requests.get(f"https://api.openbrewerydb.org/v1/breweries?page={i+1}&per_page=50")
    raw_data = json.loads(r.text)

    for raw in raw_data:
        raw_list.append(raw)

# Create DataFrame from the raw data
df = pd.DataFrame(raw_list)
df_filtered = df[df['longitude'].notna()]

df_new_york = df_filtered[df_filtered['state_province'] == 'New York']
df_new_york

geometry_newyork = gpd.points_from_xy(df_new_york['longitude'], df_new_york['latitude'], crs="EPSG:4326")


world = gpd.read_file(get_path("naturalearth.land"))
ax = world.clip([-79.7626, 40.4774,-71.8562,45.0159]).plot(color="white",edgecolor="black")


gdfNY = gpd.GeoDataFrame(df_new_york, geometry=geometry_newyork)



for x, y, city, postal_code in zip(gdfNY.geometry.x, gdfNY.geometry.y, gdfNY.city, gdfNY.postal_code):
    ax.annotate(city, xy=(x, y), xytext=(0, 3), textcoords="offset points")



gdfNY.plot(ax=ax, column="brewery_type", legend=True).set_title("New York State Open Brewery Locations and types")




print(df_filtered.head())


df_washington = df_filtered[df_filtered['state_province'] == 'Washington']

geometry_washington = gpd.points_from_xy(df_washington['longitude'], df_washington['latitude'], crs="EPSG:4326")

gdfWA = gpd.GeoDataFrame(df_washington, geometry=geometry_washington)
ax = world.clip([-124.733630, 45.543540,-116.915989,49.002494]).plot(color="white",edgecolor="black")

for x, y, city, postal_code in zip(gdfWA.geometry.x, gdfWA.geometry.y, gdfWA.city, gdfWA.postal_code):
    ax.annotate(city, xy=(x, y), xytext=(0, 3), textcoords="offset points")


gdfWA.plot(ax=ax, column="brewery_type", legend=True).set_title("Washington State Open Brewery Locations and types")


df_usa = df_filtered[df_filtered["country"]== "United States"]
geometry_usa = gpd.points_from_xy(df_usa['longitude'], df_usa['latitude'], crs="EPSG:4326")

gdfUSA = gpd.GeoDataFrame(df_usa, geometry=geometry_usa)
ax = world.clip([-124.733630, 24.520833,-66.959723,49.384358]).plot(color="white",edgecolor="black")


gdfUSA.plot(ax=ax, column="brewery_type", legend=True).set_title("United Sates Open Brewery Locations and types") 
