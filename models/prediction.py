# models/prediction.py

import pandas as pd
import torch
import os
from .model_definition import DDoSDetector # Relative import

# --- Global model loading to avoid reloading on every call ---
# This part runs only once when the module is first imported.
SCRIPT_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(SCRIPT_DIR, 'ddos_detection_model.pth')
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Assuming input dimension is known and fixed (10 in your case)
MODEL = DDoSDetector(input_dim=10).to(DEVICE)
MODEL.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
MODEL.eval()


def run_prediction(df_predict: pd.DataFrame) -> tuple[list, list]:
    """
    Runs DDoS prediction on a DataFrame containing the required features.

    This function is a pure model interface. It does not perform file I/O.

    Args:
        df_predict (pd.DataFrame): A DataFrame with the exact feature columns
                                   the model was trained on.

    Returns:
        tuple[list, list]: A tuple containing two lists:
                           - A list of prediction class strings ("DDoS" or "BENIGN").
                           - A list of prediction probability strings.
    """
    predictions_list = []
    probabilities_list = []

    with torch.no_grad():
        for index, row in df_predict.iterrows():
            # Convert row to tensor
            input_data = [row.tolist()]
            input_tensor = torch.tensor(
                input_data, dtype=torch.float32
            ).reshape(1, 1, -1).to(DEVICE)
            
            # Get model output
            output = MODEL(input_tensor)
            probability = output.item()
            
            # Determine class and format output
            predicted_class = "DDoS" if probability > 0.5 else "BENIGN"
            
            predictions_list.append(predicted_class)
            probabilities_list.append(f"{probability:.4f}")
            
    return predictions_list, probabilities_list