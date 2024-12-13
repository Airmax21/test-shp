import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# Fungsi untuk membaca dan menggabungkan banyak shapefile dalam folder
def load_and_merge_shapefiles(input_folder):
    # Daftar untuk menyimpan GeoDataFrame dari setiap shapefile
    gdfs = []
    
    # Loop untuk membaca setiap shapefile dalam folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".shp"):
            shapefile_path = os.path.join(input_folder, filename)
            try:
                gdf = gpd.read_file(shapefile_path)
                
                # Ubah CRS ke EPSG:4326 jika perlu
                if gdf.crs != "EPSG:4326":
                    gdf = gdf.to_crs(epsg=4326)
                    
                gdfs.append(gdf)
            except Exception as e:
                st.error(f"Kesalahan saat membaca {filename}: {e}")

    if not gdfs:
        st.error("Tidak ada shapefile yang valid ditemukan.")
        st.stop()

    # Menggabungkan semua GeoDataFrame menjadi satu
    merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

    return merged_gdf

# Fungsi untuk membuat peta folium dari GeoDataFrame
def create_map(gdf):
    # Mendapatkan pusat peta berdasarkan bounding box shapefile
    minx, miny, maxx, maxy = gdf.total_bounds
    map_center = [(miny + maxy) / 2, (minx + maxx) / 2]

    # Membuat peta folium
    m = folium.Map(location=map_center, zoom_start=12)

    # Menambahkan shapefile ke peta folium
    folium.GeoJson(gdf).add_to(m)

    return m

# Streamlit Interface
st.title('Peta Interaktif dari Gabungan Banyak Shapefile')

# Tentukan folder tempat shapefile berada
input_folder = "SHP"  # Ganti dengan folder tempat shapefile Anda

# Membaca dan menggabungkan shapefile
merged_gdf = load_and_merge_shapefiles(input_folder)

# Membuat peta dari gabungan shapefile
m = create_map(merged_gdf)

# Menampilkan peta interaktif di Streamlit
st_folium(m, width=725)
