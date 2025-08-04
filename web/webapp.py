import sys
from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
import pandas as pd
import os

# Add the analysis directory to Python path to import project modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'analysis'))
# Also add the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../uploads'
app.config['RESULT_FOLDER'] = '../results'

# Ensure necessary folders exist
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results'), exist_ok=True)

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
        
        # Save current filename for later use
        session_file = os.path.join(app.config['RESULT_FOLDER'], 'current_file.txt')
        with open(session_file, 'w') as f:
            f.write(filepath)
        
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
        with open(session_file, 'r') as f:
            filepath = f.read().strip()
        
        # Import and call the analysis function from the project
        from initAna import load_and_preprocess_data, feature_analysis, visualize_and_save
        
        # Process the file
        data = load_and_preprocess_data(filepath)
        feature_importance, model = feature_analysis(data)
        
        # Save current working directory and change to result directory
        original_cwd = os.getcwd()
        result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
        os.chdir(result_dir)
        
        try:
            # Visualize and save results (function doesn't accept output_dir parameter)
            visualize_and_save(feature_importance)
        finally:
            # Change back to original directory
            os.chdir(original_cwd)
        
        # Save feature importance results to session
        feature_importance.to_csv(os.path.join(app.config['RESULT_FOLDER'], 'feature_importance_results.csv'), index=False)
        feature_importance.head(10).to_csv(os.path.join(app.config['RESULT_FOLDER'], 'top_10_features.csv'), index=False)
        
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
        
        plot_file = os.path.join(app.config['RESULT_FOLDER'], 'feature_importance.png')
        plot_exists = os.path.exists(plot_file)
        
        return render_template('results.html', 
                             features=top_features.to_dict('records'),
                             plot_exists=plot_exists)
    except Exception as e:
        return f"Error loading results: {str(e)}"

@app.route('/plot')
def plot():
    plot_path = os.path.join(app.config['RESULT_FOLDER'], 'feature_importance.png')
    if os.path.exists(plot_path):
        return send_file(plot_path, mimetype='image/png')
    else:
        return "Plot not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)