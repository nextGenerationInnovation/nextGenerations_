import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from model.risk_assessment import categorize_risk
from utils.data_processing import get_real_time_data, save_data_to_log, load_data_from_log
from utils.notifications import generate_alert
import time
import plotly.express as px
import os

# Main UI design
st.set_page_config(page_title="Water Quality Monitoring System", layout="wide")

st.title("💧 Water Quality Monitoring System")
st.subheader("Real-time Monitoring and Risk Assessment")

# Sidebar for user input
st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 60, 5)

# Initialize data
data = get_real_time_data()

# Sidebar sliders for each contaminant
st.sidebar.header("Adjust Contaminant Levels")
contaminants = data['Contaminant'].unique()
slider_values = {}
for contaminant in contaminants:
    slider_values[contaminant] = st.sidebar.slider(
        f"{contaminant} Level", 0.0, 100.0, float(data[data['Contaminant'] == contaminant]['Level'].iloc[-1])
    )

# Dropdown to select contaminant
selected_contaminant = st.selectbox("Select Contaminant", contaminants)

# Dropdown to select timeframe
timeframes = {
    "5 seconds": timedelta(seconds=5),
    "1 minute": timedelta(minutes=1),
    "5 minutes": timedelta(minutes=5),
    "15 minutes": timedelta(minutes=15),
    "30 minutes": timedelta(minutes=30),
    "1 hour": timedelta(hours=1),
    "2 hours": timedelta(hours=2),
    "4 hours": timedelta(hours=4),
    "6 hours": timedelta(hours=6),
    "1 day": timedelta(days=1),
    "1 month": timedelta(days=30),
    "1/2 year": timedelta(days=182),
    "1 year": timedelta(days=365)
}
selected_timeframe = st.selectbox("Select Timeframe", list(timeframes.keys()))

# Placeholders for real-time data and plot
data_placeholder = st.empty()
plot_placeholder = st.empty()
alert_placeholder = st.empty()

# Function to update data and plot
def update_data_and_plot():
    global data
    new_data = get_real_time_data()
    for contaminant in contaminants:
        new_data.loc[new_data['Contaminant'] == contaminant, 'Level'] = np.random.uniform(0, 100)
    data = pd.concat([data, new_data]).tail(100)  # Keep the last 100 entries

    # Save data to log file
    save_data_to_log(data)

    # Load data from log file based on selected contaminant and timeframe
    filtered_data = load_data_from_log(selected_contaminant, selected_timeframe)

    # Update real-time data display
    data_placeholder.dataframe(filtered_data)

    # Risk Assessment and Alerts
    filtered_data.loc[:, 'Risk_Level'] = filtered_data.apply(categorize_risk, axis=1)
    alerts = generate_alert(filtered_data)
    alert_placeholder.empty()  # Clear previous alerts
    for alert in alerts:
        alert_placeholder.warning(alert)

    # Update plot
    fig = px.line(filtered_data, x='Time', y='Level', title=f"{selected_contaminant} Levels Over Time",
                  labels={'Time': 'Time', 'Level': 'Level'}, template='plotly_dark')
    fig.update_traces(mode='lines+markers')
    plot_placeholder.plotly_chart(fig, use_container_width=True)

# Real-time data update loop
while True:
    update_data_and_plot()
    time.sleep(refresh_rate)

