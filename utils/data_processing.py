import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def get_real_time_data():
    # Placeholder for real-time data retrieval logic.
    # For now, simulate data using random numbers.
    contaminants = ['E. coli', 'Coliform', 'Salmonella', 'Lead', 'Arsenic', 'Mercury', 'Cadmium', 'Chromium', 'Nitrates', 'Fluoride', 'Chlorine']
    data = {
        'Contaminant': contaminants,
        'Level': np.random.uniform(0, 100, len(contaminants)),
        'Time': [datetime.now() for _ in contaminants]  # Add a timestamp for each contaminant
    }
    return pd.DataFrame(data)

def save_data_to_log(data):
    # Save data to a CSV log file for each contaminant
    for contaminant in data['Contaminant'].unique():
        folder_path = f'logs/{contaminant}'
        os.makedirs(folder_path, exist_ok=True)
        file_path = f'{folder_path}/5_seconds.csv'
        data[data['Contaminant'] == contaminant].to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

def load_data_from_log(contaminant, timeframe_str):
    # Convert timeframe string to timedelta
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
    timeframe = timeframes[timeframe_str]

    folder_path = f'logs/{contaminant}'
    file_path = f'{folder_path}/5_seconds.csv'
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=['Contaminant', 'Level', 'Time'])

    data = pd.read_csv(file_path)
    data['Time'] = pd.to_datetime(data['Time'])

    end_time = datetime.now()
    start_time = end_time - timeframe
    filtered_data = data[(data['Time'] >= start_time)]

    # Aggregate data based on the selected timeframe
    if timeframe > timedelta(minutes=1):
        resample_rule = {
            "1 minute": '1T',
            "5 minutes": '5T',
            "15 minutes": '15T',
            "30 minutes": '30T',
            "1 hour": '1H',
            "2 hours": '2H',
            "4 hours": '4H',
            "6 hours": '6H',
            "1 day": '1D',
            "1 month": '1M',
            "1/2 year": '6M',
            "1 year": '1Y'
        }[timeframe_str]
        filtered_data = filtered_data.set_index('Time').resample(resample_rule).mean().reset_index()

    return filtered_data
