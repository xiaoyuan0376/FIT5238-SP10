import sys
from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
import pandas as pd
import os
import numpy as np

# Add the analysis directory to Python path to import project modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'analysis'))
# Also add the current directory and models directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models'))

app = Flask(__name__)
# Use absolute paths for upload and result folders
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads'))
app.config['RESULT_FOLDER'] = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results'))

# Ensure necessary folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Save current filename for later use - ensure absolute path
        session_file = os.path.join(app.config['RESULT_FOLDER'], 'current_file.txt')
        # Use os.path.abspath to ensure absolute path and normalize the path
        abs_filepath = os.path.abspath(filepath)
        with open(session_file, 'w') as f:
            f.write(abs_filepath)
        print(f"File saved to: {abs_filepath}")  # Debug log
        
        return redirect(url_for('analyze', filename=file.filename))

@app.route('/analyze')
def analyze():
    filename = request.args.get('filename', 'unknown')
    return render_template('analyze.html', filename=filename)

@app.route('/process', methods=['POST'])
def process_file():
    try:
        # Get the uploaded file path
        session_file = os.path.join(app.config['RESULT_FOLDER'], 'current_file.txt')
        if not os.path.exists(session_file):
            return jsonify({'status': 'error', 'message': 'No file uploaded or session expired'})
            
        with open(session_file, 'r') as f:
            filepath = os.path.abspath(f.read().strip())  # Ensure absolute path
        print(f"Processing file: {filepath}")  # Debug log
        
        # Import the analysis functions from the project - now should work with sys.path modification above
        from analysis.pca_analysis import load_and_preprocess_data_unlabeled, pca_analysis, visualize_and_save_pca
        
        # Process the file
        data = load_and_preprocess_data_unlabeled(filepath)
        feature_importance, pca_model, scaler = pca_analysis(data)
        
        # Perform DDoS detection using the predict_utils module
        from models.predict_utils import predict_ddos_traffic
        
        # Take a sample of data for classification
        sample_size = min(1000, len(data))
        data_sample = data.sample(n=sample_size, random_state=42)
        
        # Perform prediction on the sample
        # Since we don't have actual labels, we'll only show predictions
        predicted_ddos_count, predicted_benign_count = predict_ddos_traffic(data_sample)
        
        # Count actual labels in the sample - not applicable for unlabeled data
        actual_ddos_count = 0
        actual_benign_count = 0
        
        # Use absolute paths for result directory
        result_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results'))
        print(f"Changing working directory to: {result_dir}")  # Debug log
        original_cwd = os.getcwd()
        os.chdir(result_dir)
        
        try:
            # Visualize and save results
            visualize_and_save_pca(feature_importance)
        finally:
            # Change back to original directory
            os.chdir(original_cwd)
            print(f"Restored working directory to: {os.getcwd()}")  # Debug log
        
        # Save feature importance results to session
        feature_importance.to_csv(os.path.join(app.config['RESULT_FOLDER'], 'feature_importance_results.csv'), index=False)
        feature_importance.head(10).to_csv(os.path.join(app.config['RESULT_FOLDER'], 'top_10_features.csv'), index=False)
        
        # Save classification results
        classification_results = {
            'predicted_ddos_count': predicted_ddos_count,
            'predicted_benign_count': predicted_benign_count,
            'actual_ddos_count': actual_ddos_count,
            'actual_benign_count': actual_benign_count,
            'total_samples': len(data_sample)
        }
        
        # Save classification results to file
        import json
        with open(os.path.join(app.config['RESULT_FOLDER'], 'classification_results.json'), 'w') as f:
            json.dump(classification_results, f)
        
        return jsonify({'status': 'success', 'message': 'Analysis completed successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/results')
def results():
    try:
        # Read feature importance results
        importance_file = os.path.join(app.config['RESULT_FOLDER'], 'feature_importance_results.csv')
        feature_importance = pd.read_csv(importance_file)
        top_features = feature_importance.head(10)
        
        # Read classification results
        classification_file = os.path.join(app.config['RESULT_FOLDER'], 'classification_results.json')
        if os.path.exists(classification_file):
            import json
            with open(classification_file, 'r') as f:
                classification_results = json.load(f)
        else:
            classification_results = None
        
        plot_file = os.path.join(app.config['RESULT_FOLDER'], 'feature_importance.png')
        plot_exists = os.path.exists(plot_file)
        
        return render_template('results.html', 
                             features=top_features.to_dict('records'),
                             plot_exists=plot_exists,
                             classification=classification_results)
    except Exception as e:
        return f"Error loading results: {str(e)}"

@app.route('/plot')
def plot():
    plot_path = os.path.join(app.config['RESULT_FOLDER'], 'feature_importance.png')
    if os.path.exists(plot_path):
        return send_file(plot_path, mimetype='image/png')
    else:
        return "Plot not found", 404

@app.route('/download_report')
def download_report():
    try:
        # Generate a simple text report
        report_content = "DDoS Traffic Analysis Report\n"
        report_content += "=" * 30 + "\n\n"
        
        # Add feature importance
        importance_file = os.path.join(app.config['RESULT_FOLDER'], 'feature_importance_results.csv')
        if os.path.exists(importance_file):
            feature_importance = pd.read_csv(importance_file)
            report_content += "Top 10 Feature Importance Rankings (PCA Analysis):\n"
            report_content += "-" * 30 + "\n"
            top_features = feature_importance.head(10)
            for i, (index, row) in enumerate(top_features.iterrows()):
                report_content += f"{i+1}. {row['Feature']}: {row['Importance']:.6f}\n"
            report_content += "\n"
        
        # Add classification results
        classification_file = os.path.join(app.config['RESULT_FOLDER'], 'classification_results.json')
        if os.path.exists(classification_file):
            import json
            with open(classification_file, 'r') as f:
                classification_results = json.load(f)
            
            report_content += "DDoS Traffic Classification Results:\n"
            report_content += "-" * 30 + "\n"
            report_content += f"Total Samples Analyzed: {classification_results['total_samples']}\n"
            report_content += f"Predicted DDoS Traffic Count: {classification_results['predicted_ddos_count']}\n"
            report_content += f"Predicted Benign Traffic Count: {classification_results['predicted_benign_count']}\n"
            report_content += f"Predicted DDoS Traffic Percentage: {classification_results['predicted_ddos_count']/classification_results['total_samples']*100:.2f}%\n\n"
            
            # Add feature importance results
            report_content += "Feature Importance Ranking (Top 10):\n"
            report_content += "-" * 30 + "\n"
            top_features = feature_importance.head(10)
            for i, (index, row) in enumerate(top_features.iterrows()):
                report_content += f"{i+1}. {row['Feature']}: {row['Importance']:.6f}\n"
            report_content += "\n"
        
        # Save report to file
        report_path = os.path.join(app.config['RESULT_FOLDER'], 'ddos_analysis_report.txt')
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        return send_file(report_path, as_attachment=True, download_name='ddos_analysis_report.txt')
    except Exception as e:
        return f"Error generating report: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)