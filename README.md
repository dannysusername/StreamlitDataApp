# Biscayne Bay Water Quality Explorer

**Biscayne Bay Water Quality Explorer is live — just open it in your browser:**

### 👉 https://YOUR-APP-NAME.streamlit.app

No install, no setup, nothing to download. The app opens straight to the survey data. Everything below is for people who want to *develop* the explorer; if you just want to *use* it, the link above is all you need.

---

## What it is
An interactive web app for exploring one water-quality survey of Biscayne Bay, Florida, recorded by an autonomous underwater vehicle.

- **Overview**: what was measured, where and when, with summary metrics for the selected time window.
- **Interactive map**: the vehicle's survey path, with each reading coloured by the parameter you choose.
- **Time-series chart**: the parameter over the survey, with raw readings and a 60-second average.
- **Insights**: plain-language findings, all computed live from the data, such as whether oxygen stays at levels that are healthy for marine life.
- **Raw data**: an optional table of the cleaned readings.

## Dataset
`biscayneBay_waterquality.csv`: a log from an EcoMapper-style autonomous vehicle surveying Biscayne Bay on **February 4, 2022**, from 16:18 to 16:34. It contains **942 readings**, about one per second, at roughly 1 ft depth.

The raw file has 69 columns that mix vehicle telemetry (GPS, fins, battery) with readings from the water-quality sonde. The app cleans it as follows:

| Step | Why |
|---|---|
| Keep only position + sonde columns (temperature, salinity, conductance, pH, dissolved oxygen, chlorophyll, blue-green algae, depth) | Vehicle telemetry isn't water quality. A second CTD sensor duplicated temperature and salinity, so the sonde was used as the single source. |
| Strip whitespace from column names | The raw header has `"Date m/d/y   "` with trailing spaces |
| Combine date + time into one `Timestamp` | Needed for the time-series chart and the time slider |
| Clip negative chlorophyll and algae readings to 0 | Negative concentrations are sensor noise near zero |
| Exclude turbidity | ⚠️ Every turbidity reading was negative, which points to a sensor fault |

## Using it
1. **Open the app** at the link above.
2. **Pick a parameter** from the **Water-quality parameter** dropdown in the sidebar. The map and chart recolour to show it.
3. **Narrow the time window** with the **Time window** slider. Every metric, chart and insight updates to cover only that window.
4. **Tick "Show raw data table"** to see the cleaned readings behind the charts.
5. **Hover** over the map or chart for exact values. Drag to zoom; double-click to reset.

---

## Local development
A single-file Streamlit app (`app.py`) that reads the CSV committed in the repo. There's no database and there are no environment variables, so local and production run identically.

```bash
git clone https://github.com/dannysusername/StreamlitDataApp.git
cd StreamlitDataApp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Run the app:**
```bash
streamlit run app.py
```
It opens at http://localhost:8501.

## Tech stack
| Library | Role |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI, widgets and hosting (Community Cloud) |
| [pandas](https://pandas.pydata.org) | Loading and cleaning the CSV |
| [Plotly](https://plotly.com/python/) | Interactive map and time-series chart |

## Deployment
The app is hosted on **Streamlit Community Cloud**, linked to this repo's `main` branch. Every push to `main` redeploys automatically; there's no separate staging environment.

| Environment | Branch | URL |
|---|---|---|
| Production | `main` | https://YOUR-APP-NAME.streamlit.app |

- ⚠️ **Run the app locally before pushing**, because a push goes live immediately.
- Cloud installs the packages in `requirements.txt`. A missing package there is the most common cause of a failed deploy.

## Architecture
`app.py` runs top to bottom on every interaction, as all Streamlit apps do. `load_data()` (cached with `@st.cache_data`) cleans the CSV once. The sidebar widgets then filter it into `view`, and the Overview, Data Display and Insights sections all render from `view`, so every number and chart follows the controls.

---

## Agile process
- **User stories** are tracked as GitHub Issues (#1–#10), each with acceptance criteria.
- A **GitHub Projects board** (Todo / In Progress / Done) holds the backlog.
- The work ran in **three sprints**, labelled `sprint-1` to `sprint-3`:
  1. Environment and data layer
  2. Widgets and charts
  3. Insights, documentation and deployment
- **Definition of Done:** the story runs locally without errors, it's committed with a message that references its issue (`closes #N`), and its issue is closed and moved to Done.

## Sprint log
### Sprint 1
- **Done:** venv, requirements.txt, load_data, cleaned data table
- **Hard:** conda (base) and venv both active; the CSV mixes vehicle and water columns
- **Next:** add widgets and charts

### Sprint 2
- **Done:** Overview metrics, parameter dropdown, time slider, raw-data checkbox, map, time-series chart
- **Hard:** pasting indented code caused IndentationErrors and duplicate widgets; cleaning up git history
- **Next:** Insights, README, deploy

### Sprint 3
- **Done:** Insights section, README
- **Hard:**
- **Next:** deploy to Streamlit Community Cloud
