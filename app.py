import streamlit as st
import pandas as pd
import folium
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
    }[data-testid="stMetricValue"] {
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

@st.cache_data
def load_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
    df = pd.read_csv(url)
    df = df[['time', 'latitude', 'longitude', 'depth', 'mag', 'place']]
    df = df.dropna()
    df = df[df['mag'] > 0]
    return df

df = load_data()

st.sidebar.header("Filters")
min_mag, max_mag = st.sidebar.slider(
    "Magnitude Range",
    min_value=0.0,
    max_value=10.0,
    value=(2.0, 10.0),
    step=0.1
)

filtered_df = df[(df['mag'] >= min_mag) & (df['mag'] <= max_mag)]

col1, col2, col3 = st.columns(3)
col1.metric("Total Earthquakes", len(filtered_df))
col2.metric("Avg Magnitude", round(filtered_df['mag'].mean(), 2))
col3.metric("Avg Depth (km)", round(filtered_df['depth'].mean(), 2))

st.subheader("Seismic Activity Map")
m = folium.Map(location=[20, 0], zoom_start=2)

for _, row in filtered_df.iterrows():
    color = 'green' if row['mag'] < 3 else 'orange' if row['mag'] < 5 else 'red'
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['mag'] * 2,
        color=color,
        fill=True,
        fill_opacity=0.6,
        popup=f"{row['place']} | Mag: {row['mag']} | Depth: {row['depth']}km"
    ).add_to(m)

st_folium(m, width=1200, height=500)

st.subheader("Magnitude Distribution")
st.bar_chart(filtered_df['mag'].value_counts().sort_index())

st.subheader("Raw Data")
st.dataframe(filtered_df.head(100))