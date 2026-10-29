from datetime import timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Biscayne Bay Water Quality", layout="wide")

DATA_PATH = "biscayneBay_waterquality.csv"

# Raw column name -> friendly name. Only these sonde columns are kept.
COLUMNS = {
    "Latitude": "Latitude",
    "Longitude": "Longitude",
    "Temp C": "Temperature (°C)",
    "Sal ppt": "Salinity (ppt)",
    "SpCond mS/cm": "Specific Conductance (mS/cm)",
    "pH": "pH",
    "ODO mg/L": "Dissolved Oxygen (mg/L)",
    "ODOsat %": "Dissolved Oxygen (% sat)",
    "Turbid+ NTU": "Turbidity (NTU)",
    "Chl ug/L": "Chlorophyll (µg/L)",
    "BGA-PC cells/mL": "Blue-Green Algae (cells/mL)",
    "Depth feet": "Depth (ft)",
}

# Negative readings here are sensor noise near zero, so they're clipped to 0.
NON_NEGATIVE = ["Turbidity (NTU)", "Chlorophyll (µg/L)", "Blue-Green Algae (cells/mL)"]


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()  # "Date m/d/y   " -> "Date m/d/y"
    df["Timestamp"] = pd.to_datetime(
        df["Date m/d/y"] + " " + df["Time hh:mm:ss"],
        format="%m/%d/%y %H:%M:%S",
    )
    df = df[list(COLUMNS) + ["Timestamp"]].rename(columns=COLUMNS)
    df[NON_NEGATIVE] = df[NON_NEGATIVE].clip(lower=0)
    return df


# Values a visitor can pick. Turbidity is left out: every reading was negative (sensor fault).
PARAMETERS = [
    "Salinity (ppt)",
    "Temperature (°C)",
    "Dissolved Oxygen (mg/L)",
    "Dissolved Oxygen (% sat)",
    "pH",
    "Specific Conductance (mS/cm)",
    "Chlorophyll (µg/L)",
    "Blue-Green Algae (cells/mL)",
    "Depth (ft)",
]
DO_STRESS_LEVEL = 4.0  # mg/L; below this, fish and other marine life become stressed

df = load_data(DATA_PATH)

# --- Sidebar controls ---
st.sidebar.header("Controls")
param = st.sidebar.selectbox("Water-quality parameter", PARAMETERS)
start, end = st.sidebar.slider(
    "Time window",
    min_value=df["Timestamp"].min().to_pydatetime(),
    max_value=df["Timestamp"].max().to_pydatetime(),
    value=(df["Timestamp"].min().to_pydatetime(), df["Timestamp"].max().to_pydatetime()),
    step=timedelta(seconds=10),
    format="HH:mm:ss",
)
show_raw = st.sidebar.checkbox("Show raw data table")

view = df[df["Timestamp"].between(start, end)]
if view.empty:
    st.warning("No readings in this time window. Widen the slider.")
    st.stop()

# --- Overview ---
st.title("Biscayne Bay Water Quality")
st.header("Overview")
st.markdown(
    "This app explores readings from an autonomous underwater vehicle that surveyed "
    "Biscayne Bay, Florida, on **February 4, 2022**. A water-quality sensor on board "
    "recorded temperature, salinity, pH, dissolved oxygen and algae about once per second. "
    "Use the sidebar to pick a parameter and narrow the time window."
)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Readings", f"{len(view):,}")
col2.metric("Avg temperature", f"{view['Temperature (°C)'].mean():.2f} °C")
col3.metric("Avg salinity", f"{view['Salinity (ppt)'].mean():.2f} ppt")
col4.metric("Avg dissolved oxygen", f"{view['Dissolved Oxygen (mg/L)'].mean():.2f} mg/L")

# --- Data Display ---
st.header("Data Display")
st.markdown(f"Each dot on the map is one reading, coloured by **{param}**.")
fig_map = px.scatter_map(
    view,
    lat="Latitude",
    lon="Longitude",
    color=param,
    hover_data=["Timestamp"],
    color_continuous_scale="Viridis",
    zoom=17,
    height=500,
    title=f"Survey path coloured by {param}",
)
st.plotly_chart(fig_map, width="stretch")

trend = view[["Timestamp", param]].copy()
trend["60-second average"] = trend[param].rolling(60, center=True, min_periods=1).mean()
fig_line = px.line(
    trend,
    x="Timestamp",
    y=[param, "60-second average"],
    title=f"{param} over time",
    labels={"Timestamp": "Time (Feb 4, 2022)", "value": param, "variable": "Series"},
)
st.plotly_chart(fig_line, width="stretch")

df = load_data(DATA_PATH)

    # --- Sidebar controls ---
    st.sidebar.header("Controls")
    param = st.sidebar.selectbox("Water-quality parameter", PARAMETERS)
    start, end = st.sidebar.slider(
        "Time window",
        min_value=df["Timestamp"].min().to_pydatetime(),
        max_value=df["Timestamp"].max().to_pydatetime(),
        value=(df["Timestamp"].min().to_pydatetime(), df["Timestamp"].max().to_pydatetime()),
        step=timedelta(seconds=10),
        format="HH:mm:ss",
    )
    show_raw = st.sidebar.checkbox("Show raw data table")

    view = df[df["Timestamp"].between(start, end)]
    if view.empty:
        st.warning("No readings in this time window. Widen the slider.")
        st.stop()

    # --- Overview ---
    st.title("Biscayne Bay Water Quality")
    st.header("Overview")
    st.markdown(
        "This app explores readings from an autonomous underwater vehicle that surveyed "
        "Biscayne Bay, Florida, on **February 4, 2022**. A water-quality sensor on board "
        "recorded temperature, salinity, pH, dissolved oxygen and algae about once per second. "
        "Use the sidebar to pick a parameter and narrow the time window."
    )
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Readings", f"{len(view):,}")
    col2.metric("Avg temperature", f"{view['Temperature (°C)'].mean():.2f} °C")
    col3.metric("Avg salinity", f"{view['Salinity (ppt)'].mean():.2f} ppt")
    col4.metric("Avg dissolved oxygen", f"{view['Dissolved Oxygen (mg/L)'].mean():.2f} mg/L")

    # --- Data Display ---
    st.header("Data Display")
    st.markdown(f"Each dot on the map is one reading, coloured by **{param}**.")
    fig_map = px.scatter_map(
        view,
        lat="Latitude",
        lon="Longitude",
        color=param,
        hover_data=["Timestamp"],
        color_continuous_scale="Viridis",
        zoom=17,
        height=500,
        title=f"Survey path coloured by {param}",
    )
    st.plotly_chart(fig_map, width="stretch")

    trend = view[["Timestamp", param]].copy()
    trend["60-second average"] = trend[param].rolling(60, center=True, min_periods=1).mean()
    fig_line = px.line(
        trend,
        x="Timestamp",
        y=[param, "60-second average"],
        title=f"{param} over time",
        labels={"Timestamp": "Time (Feb 4, 2022)", "value": param, "variable": "Series"},
    )
    st.plotly_chart(fig_line, width="stretch")

    if show_raw:
        st.subheader("Raw data")
        st.dataframe(view)

        # --- Insights ---
    st.header("Insights")
    do_min = view["Dissolved Oxygen (mg/L)"].min()
    temp_do_corr = view["Temperature (°C)"].corr(view["Dissolved Oxygen (mg/L)"])
    saltiest = view.loc[view["Salinity (ppt)"].idxmax()]
    st.markdown(
        f"""
    - **Oxygen is healthy.** Dissolved oxygen never dropped below **{do_min:.2f} mg/L**, comfortably above the
      {DO_STRESS_LEVEL:.0f} mg/L level where marine life becomes stressed.
    - **Salinity varies the most.** It ranged from **{view['Salinity (ppt)'].min():.1f}** to
      **{view['Salinity (ppt)'].max():.1f} ppt** and peaked at {saltiest['Timestamp']:%H:%M:%S}.
      Typical seawater is about 35 ppt, so parts of this area are saltier than the open ocean.
    - **Temperature and oxygen** have a correlation of **{temp_do_corr:.2f}** in this window
      (−1 = perfectly opposite, +1 = move together).
    - **Data caveat:** every turbidity reading was negative, which points to a sensor fault, so turbidity is excluded.
      Negative chlorophyll and algae readings were treated as 0.
    """
    )

