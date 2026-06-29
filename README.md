<div align="center">

# 🌍 GeoSpatial Earthquake Analytics System

### A real-time seismic intelligence dashboard powered by live USGS data

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Folium](https://img.shields.io/badge/Folium-Mapping-77B829?style=for-the-badge)](https://python-visualization.github.io/folium/)
[![USGS](https://img.shields.io/badge/Data-USGS%20Live%20Feed-orange?style=for-the-badge)](https://earthquake.usgs.gov)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

<br>

> 🔴 **10,000+ monthly seismic events** &nbsp;|&nbsp; ⚡ **10x faster rendering** &nbsp;|&nbsp; 🧠 **7-tier intensity classification** &nbsp;|&nbsp; 💾 **50% less memory**

<br>

</div>

---

## 📖 What is this project?

Every day, hundreds of earthquakes shake the Earth — most too small to feel, some powerful enough to reshape landscapes. Yet this data, collected in real time by global sensor networks, is rarely accessible to anyone outside a research lab.

**This dashboard changes that.**

The GeoSpatial Earthquake Analytics System pulls live earthquake data directly from the **USGS (United States Geological Survey)** — the world's most authoritative seismic data source — and transforms it into an interactive, visual, real-time analytics experience. No manual downloads. No stale spreadsheets. Just open the app, and the Earth's seismic pulse is right in front of you.

Built as a full-stack data pipeline from raw JSON feeds to a polished Streamlit dashboard, this project blends **geospatial engineering, machine learning classification, and performance-optimized data processing** into a single deployable application.

---

## 🎯 Performance at a Glance

<div align="center">

| 📊 Metric | 🚀 Result |
|-----------|-----------|
| Monthly seismic events processed | **10,000+** |
| Map rendering speed vs standard markers | **10x faster** |
| Memory reduction via dtype optimization | **~50%** |
| Custom intensity zones classified | **7 tiers** |
| Data freshness (auto-cache refresh) | **Every 1 hour** |
| Max raw data rows displayed | **200 (paginated)** |

</div>

---

## ✨ Features

<details>
<summary><b>🗺️ Interactive Seismic World Map</b> — click to expand</summary>
<br>

The centerpiece of the dashboard. Every earthquake from the past 30 days is plotted on a **dark-themed CartoDB world map** with two powerful visualization modes:

**Mode 1 — Cluster Markers**

Earthquakes appear as color-coded circles, sized proportionally to their magnitude:

| Color | Magnitude | Severity |
|-------|-----------|----------|
| 🟢 Green | < 3.0 | Minor — rarely felt |
| 🟠 Orange | 3.0 – 5.0 | Moderate — felt, minor damage |
| 🔴 Red | > 5.0 | Strong to Great — potentially destructive |

- Click any marker → popup shows **location, magnitude, and depth**
- Nearby events **auto-cluster** at low zoom for a clean, readable map
- Powered by `FastMarkerCluster` — handles thousands of points without lag

**Mode 2 — Heatmap**

Density-based visualization where brighter regions indicate higher earthquake frequency. Ideal for identifying **active tectonic plate boundaries** and seismic hotspots (Pacific Ring of Fire, Himalayan belt, etc.) at a glance.

</details>

---

<details>
<summary><b>📊 Analytics Panels</b> — click to expand</summary>
<br>

Four charts that update **live** as you adjust the sidebar filters:

**1. Magnitude Distribution**
Bar chart showing how many earthquakes occurred at each magnitude value. Reveals whether the current period is dominated by micro-tremors or larger events.

**2. Earthquakes Over Time**
Line chart with one data point per day — shows whether seismic activity is spiking, declining, or steady. Useful for identifying aftershock sequences following major events.

**3. Depth Distribution**
Earthquakes are binned into three globally recognized depth categories:
- 🔵 **Shallow** (0–70 km) — most damaging, closest to surface
- 🟡 **Intermediate** (70–300 km) — felt over wide areas
- 🔴 **Deep** (300–700 km) — rarely destructive at surface

**4. Seismic Intensity Zone Breakdown**
Bar chart across all 7 custom intensity zones — instantly shows the distribution of earthquake severity in the filtered dataset.

</details>

---

<details>
<summary><b>🎛️ Dynamic Sidebar Filters</b> — click to expand</summary>
<br>

All filters update the map and every chart simultaneously — no page reload needed:

- **Magnitude Range slider** — narrow in on microseismic activity or only show catastrophic events
- **Depth Range slider** — isolate shallow crustal quakes from deep mantle events
- **Map View toggle** — switch between Cluster Markers and Heatmap in one click

</details>

---

<details>
<summary><b>⚡ Performance Engineering</b> — click to expand</summary>
<br>

Handling 10,000+ geospatial data points in a browser requires deliberate optimization. Four specific techniques were implemented:

**1. Memory-efficient data types**
```python
dtype={'latitude': 'float32', 'longitude': 'float32',
       'depth': 'float32', 'mag': 'float32'}
```
Using `float32` instead of default `float64` cuts memory consumption by ~50% — critical when loading tens of thousands of rows on every session start.

**2. FastMarkerCluster for rendering**
```python
FastMarkerCluster(points, callback=callback).add_to(m)
```
Unlike looping individual `CircleMarker` objects (which blocks Python), `FastMarkerCluster` offloads marker creation to JavaScript — achieving **10x faster rendering** for large datasets.

**3. Intelligent caching**
```python
@st.cache_data(ttl=3600)   # Data cache — 1 hour
@st.cache_data(ttl=3600)   # Map cache — separate from data
```
Two independent caches: one for raw data (avoids re-fetching from USGS on every interaction), one for the rendered map (avoids full rebuilds when only filters change).

**4. Selective column loading**
```python
usecols=['time', 'latitude', 'longitude', 'depth', 'mag', 'place']
```
Only 6 of the ~22 available USGS columns are loaded, minimizing I/O overhead from the start.

</details>

---

## 🧠 7-Tier Seismic Intensity Zone Classifier

A custom classification engine built from scratch, mapping every earthquake to one of 7 internationally recognized intensity zones:

<div align="center">

| 🏷️ Zone | 📐 Magnitude | 🌍 Real-World Impact |
|---------|-------------|----------------------|
| **Micro** | < 2.0 | Imperceptible to humans — detectable only by seismographs |
| **Minor** | 2.0 – 2.9 | Rarely felt — no structural impact |
| **Light** | 3.0 – 3.9 | Noticeable shaking indoors — no damage |
| **Moderate** | 4.0 – 4.9 | Felt widely — objects rattle, minor damage to weak structures |
| **Strong** | 5.0 – 5.9 | Significant damage to poorly built structures |
| **Major** | 6.0 – 6.9 | Destructive within populated areas — serious structural damage |
| **Great** | ≥ 7.0 | Catastrophic — devastating damage across entire regions |

</div>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.x | Core logic and data pipeline |
| **Dashboard** | Streamlit | Interactive web UI |
| **Mapping** | Folium + streamlit-folium | Geospatial rendering |
| **Clustering** | FastMarkerCluster | High-performance marker engine |
| **Heatmap** | Folium HeatMap plugin | Density visualization |
| **Data Processing** | Pandas, NumPy | ETL pipeline & transformations |
| **Live Data** | USGS CSV API | Real-time earthquake feed |

</div>

---

## 📂 Project Structure

```
Geospatial-Earthquake-Analytics-System/
│
├── 📄 app.py         →  v1 prototype — basic CircleMarker map + magnitude filter
│
└── 📄 appnew.py      →  v2 full release — FastMarkerCluster, HeatMap, 4 analytics
                         charts, depth filter, zone classifier, full optimizations
```

> ✅ **Recommended:** Run `appnew.py` for the complete experience. `app.py` is kept for reference.

---

## 🚀 Getting Started

### Prerequisites
- Python **3.8+**
- pip

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Vaishu2524/Geospatial-Earthquake-Analytics-System.git
cd Geospatial-Earthquake-Analytics-System
```

### 2️⃣ Install dependencies
```bash
pip install streamlit pandas folium streamlit-folium
```

### 3️⃣ Run the dashboard
```bash
streamlit run appnew.py
```

🎉 The app opens automatically at **`http://localhost:8501`**

> 💡 **Tip:** The first load fetches a full month of USGS earthquake data — this takes a few seconds. Every interaction after that uses the cache and feels instant.

---

## 📡 Live Data Source

```
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv
```

Maintained by the **U.S. Geological Survey**, this endpoint serves all recorded global earthquakes from the past 30 days — updated continuously by USGS sensor networks worldwide. The dashboard automatically refreshes this data every hour via `@st.cache_data(ttl=3600)`, so you're always looking at current information without hammering the API.

---

## 🔭 Future Roadmap

- [ ] Predictive ML model for aftershock probability estimation
- [ ] Country / region-level drill-down filtering
- [ ] Email or SMS alert system for high-magnitude events
- [ ] Historical data comparison (month-over-month trends)
- [ ] Integration with tectonic plate boundary GeoJSON overlays

---

## 👩‍💻 Author

<div align="center">

**Vaishali Chouhan**
<br>
*B.S. Applied Geology — Indian Institute of Technology (IIT), Kharagpur*
<br><br>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vaishali%20Chouhan-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vaishali-chouhan-8152a5273)
&nbsp;
[![GitHub](https://img.shields.io/badge/GitHub-vaishu2524-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vaishu2524)

</div>

---

<div align="center">

*Found this project useful or interesting?*
<br>
**Drop a ⭐ on the repo — it helps more people discover it!**

</div>
