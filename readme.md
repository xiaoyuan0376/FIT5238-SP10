# DDoS Traffic Detection System

## Project Overview

This project is a DDoS attack detection system based on machine learning and deep learning. The system can analyze network traffic data, identify key features affecting DDoS attacks, and use trained models to predict and analyze new network traffic.

Target users: Data scientists, researchers, and cybersecurity professionals.

Core functions:
- Feature analysis: Analyze the impact of features on DDoS detection results using machine learning algorithms
- Model training: Train deep learning models using real network traffic data
- Model prediction: Use trained models to predict DDoS attacks on new data
- Web display: Provide a friendly web interface for interactive analysis and result presentation

## Technical Architecture

### Overall Architecture
```
┌─────────────────┐
│   Web Browser    │
└─────────┬───────┘
          │ HTTP Request
┌─────────▼───────┐
│   Flask App     │
│  (webapp.py)    │
└───┬─────────┬───┘
    │         │
    │Call Analysis  │Call Prediction
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ Data Analysis │ │ Deep Learning Model │
│ Module    │ │ Module       │
└─────────┘ └──────────────┘
```

### Technology Stack
- Backend framework: Python Flask
- Data processing: pandas, numpy
- Machine learning: scikit-learn
- Deep learning: PyTorch
- Data visualization: matplotlib, seaborn
- Frontend template: Jinja2

## Module Description

### 1. Data Analysis Module (analysis/)
- **initAna.py**: Data preprocessing, feature analysis, and visualization functions
  - `load_and_preprocess_data()`: Load and clean CSV data
  - `feature_analysis()`: Perform feature importance analysis using random forest algorithm
  - `visualize_and_save()`: Generate feature importance charts and save results

### 2. Deep Learning Model Module (models/)
- **model.py**: Defines the LSTM-based DDoSDetector model
  - Multi-layer LSTM architecture for sequence data processing
  - Contains Dropout layers to prevent overfitting

- **train.py**: Model training script
  - Data preprocessing and loading
  - Model training and validation
  - Save model as .pth file

- **predict.py**: Standalone prediction script
  - Load trained model
  - Predict analysis for single data point

- **predict_utils.py**: Web application integrated prediction functionality
  - `predict_ddos_traffic()`: Provide prediction interface for web application

- **ddos_detection_model.pth**: Trained model parameter file

### 3. Web Application Module (web/)
- **webapp.py**: Flask main application file
  - File upload processing
  - Data analysis process control
  - Result display and download functionality

- **templates/**: HTML template files
  - `index.html`: File upload page
  - `analyze.html`: Analysis processing page
  - `results.html`: Result display page

## Workflow

### 1. Data Processing Workflow
1. User uploads CSV formatted network traffic data file
2. System loads and preprocesses data (cleaning, feature selection, label conversion)
3. Use random forest algorithm to analyze feature importance
4. Generate feature importance visualization charts

### 2. Prediction Analysis Workflow
1. Sample data from preprocessed data
2. Use trained LSTM model to predict DDoS attacks
3. Compare prediction results with actual labels
4. Statistics prediction accuracy

### 3. Result Display Workflow
1. Display feature importance ranking (Top 10)
2. Show prediction statistics (DDoS vs Normal traffic)
3. Provide chart visualization display

## Directory Structure

```
project/
├── analysis/           # Data analysis module
│   └── initAna.py     # Data preprocessing and feature analysis
├── models/            # Deep learning model module
│   ├── model.py       # Model definition
│   ├── train.py       # Model training
│   ├── predict.py     # Standalone prediction script
│   ├── predict_utils.py # Web integrated prediction functionality
│   └── ddos_detection_model.pth # Trained model parameters
├── web/               # Web application module
│   ├── webapp.py      # Flask main application
│   └── templates/     # HTML templates
├── uploads/           # Uploaded file storage directory
├── results/           # Analysis result storage directory
├── data/              # Sample data directory
├── requirements.txt   # Project dependencies
└── readme.md         # Project documentation
```

## Deployment and Running

### Environment Requirements
- Python 3.x
- Dependencies: flask, torch, pandas, numpy, scikit-learn, matplotlib, seaborn

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Web Application
```bash
python web/webapp.py
```

Visit http://localhost:5000 to view the application

### Standalone Script Usage
```bash
# Model training
python models/train.py

# Standalone prediction
python models/predict.py
```

## Design Features

### Modular Design
- Each functional module has clear responsibilities, facilitating maintenance and expansion
- Data processing, model training, prediction analysis, and web display functions are independent of each other

### Dual Model Strategy
- Use random forest for feature analysis to provide interpretability
- Use LSTM deep learning model for prediction to improve accuracy

### Path Management
- Use absolute paths to ensure proper operation in different environments
- Avoid file access issues caused by working directory changes

### Error Handling
- Contains comprehensive exception handling mechanisms
- Provide detailed error information for debugging