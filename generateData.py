import random
import time


from analysis_handler import process_uploaded_file
import pandas as pd

from models.prediction import run_prediction
import os

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
def process_uploaded_file(upload_filepath: str,n: int,output_filepath:str) -> tuple:
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


    all_cols = pd.read_csv(upload_filepath, nrows=0).columns.tolist()
    if source_ip_col in all_cols:
        cols_to_read.append(source_ip_col)
    try:
        header = pd.read_csv(upload_filepath, nrows=0).columns.tolist()
    # df_full = pd.read_csv(upload_filepath, usecols=lambda c: c in cols_to_read, low_memory=False)

        df_line = pd.read_csv(
            upload_filepath,
            skiprows=n,
            nrows=1,
            header=None,
            names=header
        )
        df_predict = df_line[required_columns].copy()
    except Exception as e:
         raise Exception(f"Error processing file: {e}")


    predictions_list, probabilities_list = run_prediction(df_predict)
    df_line['Prediction_Class'] = predictions_list
    df_line['Prediction_Probability'] = probabilities_list
    df_line['Risk_Score'] = df_line['Prediction_Probability'].apply(_map_risk_score)
    # --- REVERTED: Alert now triggers for 'Critical' ONLY ---
    df_line['Alert_Triggered'] = df_line['Risk_Score'].apply(lambda x: "YES" if x == "Critical" else "NO")

    header_needed = not os.path.exists(output_filepath)

    df_line.to_csv(
        output_filepath,
        mode='a',
        header=header_needed,
        index=False
    )
    return df_line
print("Start generate Data")
while(1):

    csv_File_Path = "random_test_sets/random_test_sets/random_test_set_1.csv"
    random_number = random.randint(1, 800)
    print('generate data:')
    print(process_uploaded_file(csv_File_Path,random_number,"222/generate.csv"))

    time.sleep(1)