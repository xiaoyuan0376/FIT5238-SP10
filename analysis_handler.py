# analysis_handler.py

import pandas as pd
from models.prediction import run_prediction
import os
from datetime import datetime

def _map_risk_score(probability: float) -> str:
    """
    UPDATED: Reverted to the original, stricter risk thresholds.
    """
    try:
        prob_val = float(probability)
    except (ValueError, TypeError):
        return "Unknown"

    # --- REVERTED to original thresholds ---
    if prob_val > 0.95:
        return "Critical"
    elif prob_val > 0.8:
        return "High"
    elif prob_val > 0.5:
        return "Medium"
    else:
        return "Low"

def process_uploaded_file(upload_filepath: str, report_dir: str, original_filename: str) -> tuple:
    """
    Orchestrates the full analysis process using the original thresholds.
    """
    required_columns = [
        " Fwd Packet Length Mean", " Fwd Packet Length Max", " Avg Fwd Segment Size",
        "Init_Win_bytes_forward", " Subflow Fwd Bytes", "Total Length of Fwd Packets",
        " act_data_pkt_fwd", " Bwd Packet Length Min", "Subflow Fwd Packets",
        " Fwd IAT Std"
    ]
    cols_to_read = required_columns.copy()
    source_ip_col = ' Source IP'
    
    try:
        all_cols = pd.read_csv(upload_filepath, nrows=0).columns.tolist()
        if source_ip_col in all_cols:
            cols_to_read.append(source_ip_col)
        df_full = pd.read_csv(upload_filepath, usecols=lambda c: c in cols_to_read, low_memory=False)
        df_predict = df_full[required_columns].copy()
    except Exception as e:
        raise Exception(f"Error processing file: {e}")

    # Run prediction and apply reverted logic
    predictions_list, probabilities_list = run_prediction(df_predict)
    df_full['Prediction_Class'] = predictions_list
    df_full['Prediction_Probability'] = probabilities_list
    df_full['Risk_Score'] = df_full['Prediction_Probability'].apply(_map_risk_score)
    # --- REVERTED: Alert now triggers for 'Critical' ONLY ---
    df_full['Alert_Triggered'] = df_full['Risk_Score'].apply(lambda x: "YES" if x == "Critical" else "NO")

    # The rest of the logic remains unchanged and will use the updated columns automatically
    total_flows = len(df_full)
    ddos_flows = predictions_list.count("DDoS")
    benign_flows = total_flows - ddos_flows
    ddos_percentage = (ddos_flows / total_flows) * 100 if total_flows > 0 else 0
    
    top_attackers_string = "Not available (Source IP column not found)."
    if source_ip_col in df_full.columns:
        ddos_traffic = df_full[df_full['Prediction_Class'] == 'DDoS']
        if not ddos_traffic.empty:
            top_attackers = ddos_traffic[source_ip_col].value_counts().nlargest(5)
            top_attackers_string = "\n".join([f"    - {ip}: {count} flows" for ip, count in top_attackers.items()])
        else:
            top_attackers_string = "No DDoS traffic detected."

    # Generate Full Report
    full_report_filename = f"report_{original_filename}"
    full_report_filepath = os.path.join(report_dir, full_report_filename)
    with open(full_report_filepath, 'w', encoding='utf-8') as f:
        # Writing the full report header
        f.write("###################################################\n#            DDoS Analysis Report                 #\n###################################################\n\n")
        f.write(f"Analysis Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write(f"Original Filename: {original_filename}\n\n")
        f.write("--- Summary ---\n")
        f.write(f"Total Flows Analyzed: {total_flows}\nBenign Flows Detected: {benign_flows}\nDDoS Flows Detected: {ddos_flows}\nDDoS Traffic Percentage: {ddos_percentage:.2f}%\n\n")
        f.write("--- Threat Intelligence ---\nTop 5 Attacking Source IPs:\n")
        f.write(f"{top_attackers_string}\n\n")
        f.write("###################################################\n#                  Full Data Log                  #\n###################################################\n\n")
        df_full.to_csv(f, index=False)

    # Generate Alert-Only Report
    df_alerts = df_full[df_full['Alert_Triggered'] == 'YES'].copy()
    alert_report_filename = None
    if not df_alerts.empty:
        alert_report_filename = f"alerts_{original_filename}"
        alert_report_filepath = os.path.join(report_dir, alert_report_filename)
        df_alerts.to_csv(alert_report_filepath, index=False)

    # Prepare Data for UI
    summary = {
        'total_rows': total_flows,
        'benign': benign_flows,
        'ddos': ddos_flows,
        'alerts': len(df_alerts),
        'ddos_percentage': f"{ddos_percentage:.2f}",
        'top_attackers_string': top_attackers_string
    }
    
    display_predictions = []
    for i in range(min(len(df_full), 1000)):
        display_predictions.append({'row_index': i + 2, 'prediction': df_full.iloc[i]['Prediction_Class'], 'probability': df_full.iloc[i]['Prediction_Probability'], 'risk_score': df_full.iloc[i]['Risk_Score'], 'alert_triggered': df_full.iloc[i]['Alert_Triggered']})
        
    display_alerts = []
    for index, row in df_alerts.iterrows():
        display_alerts.append({'row_index': index + 2, 'prediction': row['Prediction_Class'], 'probability': row['Prediction_Probability'], 'risk_score': row['Risk_Score'], 'alert_triggered': row['Alert_Triggered']})

    return (display_predictions, display_alerts, summary, full_report_filename, alert_report_filename)