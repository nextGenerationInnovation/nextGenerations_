from utils.thresholds import thresholds

def categorize_risk(row):
    contaminant = row['Contaminant']
    level = row['Level']

    if level <= thresholds[contaminant]['low']:
        return "Low"
    elif thresholds[contaminant]['low'] < level <= thresholds[contaminant]['medium']:
        return "Medium"
    elif thresholds[contaminant]['medium'] < level <= thresholds[contaminant]['high']:
        return "High"
    else:
        return "Critical"
