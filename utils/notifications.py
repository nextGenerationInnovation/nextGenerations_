def generate_alert(data):
    alerts = []
    for index, row in data.iterrows():
        if row['Risk_Level'] == "Medium":
            alerts.append(f"⚠️ {row['Contaminant']} levels are elevated. Increased monitoring needed.")
        elif row['Risk_Level'] == "High":
            alerts.append(f"🔶 {row['Contaminant']} levels require immediate attention.")
        elif row['Risk_Level'] == "Critical":
            alerts.append(f"🚨 {row['Contaminant']} levels are critical! Emergency response required.")
    return alerts


