import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from model.risk_assessment import categorize_risk
from utils.data_processing import get_real_time_data
from utils.notifications import generate_alert
import time
import plotly.express as px

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

# Placeholders for real-time data and plot
data_placeholder = st.empty()
plot_placeholder = st.empty()

# Function to update data and plot
def update_data_and_plot():
    global data
    new_data = get_real_time_data()
    for contaminant, level in slider_values.items():
        new_data.loc[new_data['Contaminant'] == contaminant, 'Level'] = level
    data = pd.concat([data, new_data]).tail(100)  # Keep the last 100 entries

    # Update real-time data display
    data_placeholder.dataframe(data)

    # Risk Assessment and Alerts
    data['Risk_Level'] = data.apply(categorize_risk, axis=1)
    alerts = generate_alert(data)
    for alert in alerts:
        st.warning(alert)

    # Update plot
    fig = px.line(data, x='Time', y='Level', color='Contaminant', title="Contaminant Levels Over Time",
                  labels={'Time': 'Time', 'Level': 'Level'}, template='plotly_dark')
    fig.update_traces(mode='lines+markers')
    plot_placeholder.plotly_chart(fig, use_container_width=True)

# Real-time data update loop
while True:
    update_data_and_plot()
    time.sleep(refresh_rate)

