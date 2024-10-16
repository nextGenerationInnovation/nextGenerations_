import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

def get_sample_data():
    # Generate sample data for visualization
    contaminants = ['E. coli', 'Coliform', 'Salmonella', 'Lead', 'Arsenic', 'Mercury', 'Cadmium', 'Chromium', 'Nitrates', 'Fluoride', 'Chlorine']
    time_range = [datetime.now() - timedelta(days=i) for i in range(30)]
    data = []
    for contaminant in contaminants:
        for time in time_range:
            data.append({
                'Contaminant': contaminant,
                'Level': np.random.uniform(0, 100),
                'Time': time
            })
    return pd.DataFrame(data)


