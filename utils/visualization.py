import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def plot_trend(data):
    st.subheader("Contaminant Levels Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='Time', y='Level', hue='Contaminant', data=data, ax=ax)
    ax.set_title("Contaminant Levels Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Level")
    st.pyplot(fig)

def plot_risk_levels(data):
    st.subheader("Risk Levels")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='Contaminant', y='Level', hue='Risk_Level', data=data, ax=ax)
    st.pyplot(fig)