import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from model.risk_assessment import categorize_risk
from utils.data_processing import get_sample_data
from utils.visualization import plot_trend
from utils.notifications import generate_alert

# Main UI design
st.set_page_config(page_title="Water Quality Monitoring System", layout="wide")

st.title("💧 Water Quality Monitoring System")
st.subheader("Real-time Monitoring and Risk Assessment")

# Sidebar for user input
st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 60, 10)

# Sample data for visualization
data = get_sample_data()

# Sidebar sliders for each contaminant
st.sidebar.header("Adjust Contaminant Levels")
contaminants = data['Contaminant'].unique()
slider_values = {}
for contaminant in contaminants:
    slider_values[contaminant] = st.sidebar.slider(
        f"{contaminant} Level", 0.0, 100.0, float(data[data['Contaminant'] == contaminant]['Level'].iloc[-1])
    )

# Update data with slider values
for contaminant, level in slider_values.items():
    data.loc[data['Contaminant'] == contaminant, 'Level'] = level

# Real-Time Data Display
st.header("Real-Time Data")
st.dataframe(data)

# Risk Assessment and Alerts
st.header("Risk Levels")
data['Risk_Level'] = data.apply(categorize_risk, axis=1)
st.write(data[['Contaminant', 'Level', 'Risk_Level']])

# Generate alerts based on risk levels
alerts = generate_alert(data)
for alert in alerts:
    st.warning(alert)

# Graphs & Trends
st.header("Trends & Historical Data")
plot_trend(data)

st.sidebar.write("Data last updated: ", pd.Timestamp.now())
st.sidebar.write("Note: Thresholds are based on EPA and WHO guidelines.")


