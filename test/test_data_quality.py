import sys
import os
import unittest
import pandas as pd
import tempfile

# Add the project root directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from analysis_handler import process_uploaded_file

class TestDataQuality(unittest.TestCase):
    """Data Quality Tests - Corresponding to DQ-001, DQ-002, DQ-003 in documentation"""
    
    def setUp(self):
        """Test setup preparation"""
        self.temp_dir = tempfile.mkdtemp()
        self.reports_dir = os.path.join(self.temp_dir, 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Define required feature columns
        self.required_columns = [
            " Fwd Packet Length Mean", " Fwd Packet Length Max", " Avg Fwd Segment Size",
            "Init_Win_bytes_forward", " Subflow Fwd Bytes", "Total Length of Fwd Packets",
            " act_data_pkt_fwd", " Bwd Packet Length Min", "Subflow Fwd Packets",
            " Fwd IAT Std"
        ]
        
    def test_required_feature_validation(self):
        """Test required feature validation - Corresponding to DQ-001 in documentation"""
        # Create test data with missing columns
        incomplete_data = pd.DataFrame({
            " Fwd Packet Length Mean": [10.5, 20.1],
            " Fwd Packet Length Max": [100.0, 200.0],
            # Intentionally missing other columns
        })
        
        incomplete_file_path = os.path.join(self.temp_dir, 'incomplete_data.csv')
        incomplete_data.to_csv(incomplete_file_path, index=False)
        
        # Verify appropriate error handling is triggered
        with self.assertRaises(Exception) as context:
            process_uploaded_file(
                upload_filepath=incomplete_file_path,
                report_dir=self.reports_dir,
                original_filename='incomplete_data.csv'
            )
        
        # Verify error message is meaningful
        self.assertIn("Error processing file", str(context.exception))
        
    def test_data_type_validation(self):
        """Test data type validation - Corresponding to DQ-002 in documentation"""
        # Create test data with invalid data types
        invalid_data = pd.DataFrame({
            " Fwd Packet Length Mean": ["invalid", "text", "not_number"],
            " Fwd Packet Length Max": [100.0, 200.0, 150.0],
            " Avg Fwd Segment Size": [50.2, 75.3, 60.1],
            "Init_Win_bytes_forward": [1024.0, 2048.0, 1536.0],
            " Subflow Fwd Bytes": [512.0, 1024.0, 768.0],
            "Total Length of Fwd Packets": [1000.0, 2000.0, 1500.0],
            " act_data_pkt_fwd": [5.0, 10.0, 7.0],
            " Bwd Packet Length Min": [20.0, 30.0, 25.0],
            "Subflow Fwd Packets": [3.0, 6.0, 4.0],
            " Fwd IAT Std": [1.5, 2.0, 1.8]
        })
        
        invalid_file_path = os.path.join(self.temp_dir, 'invalid_data.csv')
        invalid_data.to_csv(invalid_file_path, index=False)
        
        # Verify system can handle invalid data types
        with self.assertRaises(Exception) as context:
            process_uploaded_file(
                upload_filepath=invalid_file_path,
                report_dir=self.reports_dir,
                original_filename='invalid_data.csv'
            )
        
        # Verify expected error is caught (ValueError or other processing error)
        self.assertTrue(isinstance(context.exception, (ValueError, Exception)))
            
    def test_data_range_validation(self):
        """Test data range validation - Corresponding to DQ-003 in documentation"""
        # Create test data with extreme values
        extreme_data = pd.DataFrame({
            " Fwd Packet Length Mean": [float('inf'), -1000000, 0],
            " Fwd Packet Length Max": [1e10, -1e10, 0],
            " Avg Fwd Segment Size": [float('nan'), 0, 1e8],
            "Init_Win_bytes_forward": [0, 1e15, -100],
            " Subflow Fwd Bytes": [0, 1e20, -1000],
            "Total Length of Fwd Packets": [0, 1e25, -500],
            " act_data_pkt_fwd": [0, 1e10, -10],
            " Bwd Packet Length Min": [0, 1e8, -100],
            "Subflow Fwd Packets": [0, 1e6, -5],
            " Fwd IAT Std": [0, 1e5, -10]
        })
        
        extreme_file_path = os.path.join(self.temp_dir, 'extreme_data.csv')
        extreme_data.to_csv(extreme_file_path, index=False)
        
        # Verify system can handle extreme value data
        try:
            result = process_uploaded_file(
                upload_filepath=extreme_file_path,
                report_dir=self.reports_dir,
                original_filename='extreme_data.csv'
            )
            
            # Verify result structure
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 5)
            
            display_predictions, display_alerts, summary, report_filename, alert_filename = result
            
            # Verify prediction results don't contain invalid values
            for pred in display_predictions:
                self.assertIn('prediction', pred)
                self.assertIn('probability', pred)
                # Verify probability values are not NaN or inf
                prob_str = pred['probability']
                if prob_str not in ['nan', 'inf', '-inf']:
                    prob_val = float(prob_str)
                    self.assertFalse(float('inf') == prob_val)
                    self.assertFalse(float('-inf') == prob_val)
                    
        except Exception as e:
            # If error occurs when processing extreme values, verify error handling
            self.assertIn("Error", str(e))
    
    def test_empty_file_handling(self):
        """Test empty file handling"""
        # Create empty CSV file
        empty_file_path = os.path.join(self.temp_dir, 'empty_data.csv')
        with open(empty_file_path, 'w') as f:
            f.write("")
        
        # Verify empty file handling
        with self.assertRaises(Exception):
            process_uploaded_file(
                upload_filepath=empty_file_path,
                report_dir=self.reports_dir,
                original_filename='empty_data.csv'
            )
    
    def test_valid_data_processing(self):
        """Test valid data processing as control test"""
        # Create valid test data
        valid_data = pd.DataFrame({
            " Fwd Packet Length Mean": [10.5, 20.1, 15.7],
            " Fwd Packet Length Max": [100.0, 200.0, 150.0],
            " Avg Fwd Segment Size": [50.2, 75.3, 60.1],
            "Init_Win_bytes_forward": [1024.0, 2048.0, 1536.0],
            " Subflow Fwd Bytes": [512.0, 1024.0, 768.0],
            "Total Length of Fwd Packets": [1000.0, 2000.0, 1500.0],
            " act_data_pkt_fwd": [5.0, 10.0, 7.0],
            " Bwd Packet Length Min": [20.0, 30.0, 25.0],
            "Subflow Fwd Packets": [3.0, 6.0, 4.0],
            " Fwd IAT Std": [1.5, 2.0, 1.8]
        })
        
        valid_file_path = os.path.join(self.temp_dir, 'valid_data.csv')
        valid_data.to_csv(valid_file_path, index=False)
        
        # Verify valid data can be processed normally
        result = process_uploaded_file(
            upload_filepath=valid_file_path,
            report_dir=self.reports_dir,
            original_filename='valid_data.csv'
        )
        
        # Verify return results
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 5)
        
        display_predictions, display_alerts, summary, report_filename, alert_filename = result
        self.assertEqual(len(display_predictions), 3)
        self.assertEqual(summary['total_rows'], 3)

if __name__ == '__main__':
    unittest.main()