import streamlit as st
import pandas as pd
import folium
from folium.plugins import FastMarkerCluster, HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="Earthquake Analytics", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .stMetric {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 10px;
    }
    .stSidebar {
        background: rgba(255,255,255,0.05);
    }
    h1, h2, h3 {
        color: white !important;
    }
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #cccccc !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 GeoSpatial Earthquake Analytics System")
st.markdown("Visualizing global seismic activity from historical data")

@st.cache_data(ttl=3600)  
def load_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
    df = pd.read_csv(
        url,
        usecols=['time', 'latitude', 'longitude', 'depth', 'mag', 'place'],
        dtype={'latitude': 'float32', 'longitude': 'float32',  # float32 saves ~50% memory vs float64
               'depth': 'float32', 'mag': 'float32'}
    )
    df = df.dropna()
    df = df[df['mag'] > 0]
    df['time'] = pd.to_datetime(df['time'], utc=True)
    df['date'] = df['time'].dt.date
    df.sort_values('mag', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

df = load_data()

st.sidebar.header("Filters")

min_mag, max_mag = st.sidebar.slider(
    "Magnitude Range",
    min_value=0.0, max_value=10.0,
    value=(2.0, 10.0), step=0.1
)

min_depth, max_depth = st.sidebar.slider(
    "Depth Range (km)",
    min_value=float(df['depth'].min()),
    max_value=float(df['depth'].max()),
    value=(0.0, 300.0), step=1.0
)

map_style = st.sidebar.radio(
    "Map View",
    ["Cluster Markers", "Heatmap"],
    index=0
)

mask = (
    (df['mag'] >= min_mag) & (df['mag'] <= max_mag) &
    (df['depth'] >= min_depth) & (df['depth'] <= max_depth)
)
filtered_df = df[mask]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Earthquakes", f"{len(filtered_df):,}")
col2.metric("Avg Magnitude",     round(float(filtered_df['mag'].mean()), 2) if len(filtered_df) else "—")
col3.metric("Avg Depth (km)",    round(float(filtered_df['depth'].mean()), 2) if len(filtered_df) else "—")
col4.metric("Max Magnitude",     round(float(filtered_df['mag'].max()), 2) if len(filtered_df) else "—")


st.subheader("Seismic Activity Map")

def mag_to_color(mag):
    if mag < 3:   return 'green'
    elif mag < 5: return 'orange'
    else:         return 'red'

@st.cache_data(ttl=3600)
def build_map(df_json, style):
    """Cache the rendered map so filters don't rebuild it from scratch each time."""
    data = pd.read_json(df_json)
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter", scrollWheelZoom=False, zoom_control=False)

    if style == "Heatmap":
        heat_data = data[['latitude', 'longitude', 'mag']].values.tolist()
        HeatMap(heat_data, radius=8, blur=12, min_opacity=0.3).add_to(m)

    else:
        callback = """
        function(row) {
            var mag   = row[2];
            var color = mag < 3 ? 'green' : mag < 5 ? 'orange' : 'red';
            var marker = L.circleMarker(
                new L.LatLng(row[0], row[1]),
                { radius: mag * 2, color: color, fillColor: color,
                  fillOpacity: 0.6, weight: 1 }
            );
            marker.bindPopup(
                '<b>' + row[3] + '</b><br>Mag: ' + mag + '<br>Depth: ' + row[4] + ' km'
            );
            return marker;
        }
        """
        points = data[['latitude', 'longitude', 'mag', 'place', 'depth']].values.tolist()
        FastMarkerCluster(points, callback=callback).add_to(m)

    return m

if len(filtered_df) == 0:
    st.warning("No earthquakes match current filters.")
else:
    m = build_map(
        filtered_df[['latitude', 'longitude', 'mag', 'place', 'depth']].to_json(),
        map_style
    )
    st_folium(m, width=1200, height=500, returned_objects=[])

st.subheader("Magnitude Distribution")
mag_counts = filtered_df['mag'].round(1).value_counts().sort_index()
st.bar_chart(mag_counts)

st.subheader("Earthquakes Over Time")
if 'date' in filtered_df.columns:
    time_series = filtered_df.groupby('date').size().reset_index(name='count')
    st.line_chart(time_series.set_index('date')['count'])

st.subheader("Depth Distribution")
depth_bins = pd.cut(
    filtered_df['depth'],
    bins=[0, 70, 300, 700],
    labels=['Shallow (0-70 km)', 'Intermediate (70-300 km)', 'Deep (300-700 km)']
)
st.bar_chart(depth_bins.value_counts())

st.subheader("Seismic Intensity Zone Breakdown")

def classify_zone(mag):
    if mag < 2.0:  return 'Micro'
    elif mag < 3.0: return 'Minor'
    elif mag < 4.0: return 'Light'
    elif mag < 5.0: return 'Moderate'
    elif mag < 6.0: return 'Strong'
    elif mag < 7.0: return 'Major'
    else:           return 'Great'
filtered_df = filtered_df.copy()
filtered_df['zone'] = filtered_df['mag'].map(classify_zone)
zone_counts = filtered_df['zone'].value_counts().reindex(
    ['Micro', 'Minor', 'Light', 'Moderate', 'Strong', 'Major', 'Great'], fill_value=0
)
st.bar_chart(zone_counts)
st.subheader("Raw Data")
st.dataframe(
    filtered_df[['time', 'place', 'mag', 'depth', 'latitude', 'longitude', 'zone']]
    .head(200),   
    use_container_width=True
)