# milestone1_dashboard.py

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# Simulated Air Quality Dataset
# ------------------------------
date_rng = pd.date_range(start="2023-01-01", end="2023-01-07", freq="H")
np.random.seed(42)
data = {
    "datetime": date_rng,
    "PM2.5": np.random.normal(60, 15, len(date_rng)).clip(5, 250),
    "PM10": np.random.normal(100, 25, len(date_rng)).clip(10, 400),
    "NO2": np.random.normal(30, 8, len(date_rng)).clip(2, 150),
    "O3": np.random.normal(20, 5, len(date_rng)).clip(1, 120),
    "SO2": np.random.normal(15, 4, len(date_rng)).clip(1, 80),
    "CO": np.random.normal(1, 0.3, len(date_rng)).clip(0.1, 5),
}
df = pd.DataFrame(data)
df.set_index("datetime", inplace=True)

# ------------------------------
# Streamlit Dashboard
# ------------------------------
st.set_page_config(page_title="Air Quality Data Explorer", layout="wide")

st.title("🌍 Air Quality Data Explorer")
st.subheader("Milestone 1: Data Preprocessing & EDA")

# Sidebar Controls
st.sidebar.header("Data Controls")
time_range = st.sidebar.selectbox("Select Time Range", ["Last 24 Hours", "Last 3 Days", "Full Dataset"])
pollutant = st.sidebar.selectbox("Select Pollutant", df.columns)

# Filter dataset by time
if time_range == "Last 24 Hours":
    df_filtered = df.last("24H")
elif time_range == "Last 3 Days":
    df_filtered = df.last("72H")
else:
    df_filtered = df.copy()

# ------------------------------
# Layout with columns
# ------------------------------
col1, col2 = st.columns([2, 1])

# Time series plot
with col1:
    st.markdown(f"### {pollutant} Time Series")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_filtered.index, df_filtered[pollutant], marker="o", linestyle="-")
    ax.set_ylabel("Concentration (µg/m³)")
    ax.set_xlabel("Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Correlation heatmap
with col2:
    st.markdown("### Pollutant Correlations")
    fig, ax = plt.subplots(figsize=(4, 4))
    sns.heatmap(df_filtered.corr(), annot=True, cmap="Greens", fmt=".2f", ax=ax)
    st.pyplot(fig)

# ------------------------------
# Summary Statistics
# ------------------------------
st.markdown("### 📊 Statistical Summary")
stats = df_filtered[pollutant].describe()
st.write(pd.DataFrame({
    "Mean": [round(stats["mean"], 2)],
    "Median": [round(df_filtered[pollutant].median(), 2)],
    "Max": [round(stats["max"], 2)],
    "Min": [round(stats["min"], 2)],
    "Std Dev": [round(stats["std"], 2)],
    "Data Points": [len(df_filtered[pollutant])]
}))

# ------------------------------
# Distribution Analysis
# ------------------------------
st.markdown("### 📈 Distribution Analysis")
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(df_filtered[pollutant], bins=10, kde=False, ax=ax, color="green")
ax.set_xlabel(f"{pollutant} Concentration (µg/m³)")
ax.set_ylabel("Frequency")
st.pyplot(fig)
