import pandas as pd
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


st.title("Biscayne Bay Water Quality")
df = load_data(DATA_PATH)
st.dataframe(df)