import torch
import numpy as np
import os
import pandas as pd

from models.model import DDoSDetector

def predict_ddos_traffic(data_sample, model_path=None):
    """
    Predict DDoS traffic using the trained model
    
    Args:
        data_sample: DataFrame with the sample data to predict
        model_path: Path to the model file (optional)
        
    Returns:
        tuple: (predicted_ddos_count, predicted_benign_count)
    """
    try:
        # Setup device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Select only the features used in the pre-trained model (10 features)
        features_used_in_model = [" Fwd Packet Length Mean", " Fwd Packet Length Max", " Avg Fwd Segment Size",
                                "Init_Win_bytes_forward", " Subflow Fwd Bytes", "Total Length of Fwd Packets",
                                " act_data_pkt_fwd", " Bwd Packet Length Min", "Subflow Fwd Packets",
                                " Fwd IAT Std"]
        
        # Filter data to only include features that exist in the dataset
        available_features = [f for f in features_used_in_model if f in data_sample.columns]
        
        # If we don't have enough features, we can't make predictions
        if len(available_features) < len(features_used_in_model):
            print(f"Warning: Only {len(available_features)} out of {len(features_used_in_model)} required features found")
            if len(available_features) == 0:
                # If none of the specific features are available, use the first 10 features
                available_features = list(data_sample.columns[:10])
                # Remove the result column if it's in the features
                if 'result' in available_features:
                    available_features.remove('result')
        
        X_filtered = data_sample[available_features]
        
        # Load the trained model
        if model_path is None:
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ddos_detection_model.pth')
        
        # Ensure the input dimension matches the model
        model = DDoSDetector(input_dim=len(available_features)).to(device)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        
        # Reshape to 3D tensor as expected by the LSTM model
        sample_data_reshaped = X_filtered.values.reshape(X_filtered.shape[0], 1, X_filtered.shape[1])
        sample_tensor = torch.tensor(sample_data_reshaped, dtype=torch.float32).to(device)
        
        # Predict DDoS traffic
        with torch.no_grad():
            output = model(sample_tensor)
            # Use 0.5 as threshold for binary classification
            predictions = (output > 0.5).int().cpu().numpy()
        
        # Count DDoS vs Benign traffic
        predicted_ddos_count = int(np.sum(predictions))
        predicted_benign_count = len(predictions) - predicted_ddos_count
        
        return predicted_ddos_count, predicted_benign_count
    except Exception as e:
        print(f"Error in predict_ddos_traffic: {str(e)}")
        # Return default values in case of error
        return 0, len(data_sample) if 'data_sample' in locals() else 0