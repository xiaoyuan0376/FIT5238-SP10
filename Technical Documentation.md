# Technical Documentation: DDoS Traffic Analysis System

### 1. Overview

#### 1.1. Project Purpose
The DDoS Traffic Analysis System is a web-based application designed to provide a user-friendly interface for analyzing network traffic data from CSV files. Users can upload a file, and the system leverages a pre-trained deep learning model to predict whether each traffic flow is `BENIGN` or part of a `DDoS` attack. The system generates comprehensive analysis results, including detailed reports, risk assessments, and a focused summary of high-risk "alert" traffic.

#### 1.2. Core Technologies
*   **Backend Framework:** Python with Flask
*   **AI/ML Framework:** PyTorch
*   **Data Manipulation:** Pandas & NumPy
*   **Frontend:** HTML5, CSS3, JavaScript (Jinja2 for templating)
*   **Core AI Model:** A stacked Long Short-Term Memory (LSTM) network

#### 1.3. Target Audience
This document is intended for software developers, system architects, and data scientists involved in the maintenance, deployment, or future development of this system.

---

### 2. System Design & Architecture

#### 2.1. Architectural Style
The system is designed as a **Monolithic Web Application** following a **Layered Architecture**, emphasizing a clear **Separation of Concerns**.

*   **Presentation Layer:** Comprised of `app.py` and the `templates/` & `static/` directories. It is responsible for handling user interaction and rendering pages.
*   **Business Logic Layer:** The core of this layer is `analysis_handler.py`. It is responsible for orchestrating the entire analysis workflow.
*   **Data Access / Model Layer:** Encapsulated within the `models/` directory. It handles all interactions with the AI model.

This layered approach ensures that each part of the application can be modified and tested independently. For example, the UI can be updated without affecting the backend logic.

#### 2.2. Project Structure
```
DDoS_Traffic_Analysis_System/
|
|-- app.py                      # Core Flask application (Presentation Layer)
|-- analysis_handler.py         # Business Logic Layer
|-- requirements.txt
|
|-- models/                     # Data Access / Model Layer
|   |-- __init__.py
|   |-- model_definition.py       # Model architecture definition
|   |-- prediction.py             # Model inference interface
|   |-- ddos_detection_model.pth  # Model weights
|
|-- static/                     # Static assets (Presentation Layer)
|-- templates/                  # HTML templates (Presentation Layer)
|
|-- uploads/                    # (Auto-created) User-uploaded files
|-- reports/                    # (Auto-created) Generated reports
```

#### 2.3. Data Flow
The typical user workflow triggers the following data flow:
1.  **Upload:** User selects a CSV file and submits the form on the `index.html` page.
2.  **Request Handling:** `app.py` receives the `POST` request, saves the file to the `/uploads` directory, and calls `process_uploaded_file()` in `analysis_handler.py`.
3.  **Data Processing:** `analysis_handler.py` reads the CSV into a Pandas DataFrame and validates the required feature columns.
4.  **Prediction:** `analysis_handler.py` passes the feature DataFrame to the `run_prediction()` function in `models/prediction.py`.
5.  **Inference:** `models/prediction.py` iterates through the data, converts each row into a PyTorch tensor, and feeds it into the pre-loaded model to get prediction probabilities.
6.  **Post-Processing & Reporting:** `analysis_handler.py` receives the predictions, enhances the DataFrame with new columns (`Risk_Score`, `Alert_Triggered`), calculates summaries, and saves the full and alert-only reports to the `/reports` directory.
7.  **Response Generation:** `analysis_handler.py` returns a tuple containing all necessary data (UI previews, summaries, report filenames) back to `app.py`.
8.  **Rendering:** `app.py` renders the `results.html` template, passing all the processed data into it for display.
9.  **Download:** If the user clicks a download button, the `download_report()` route in `app.py` serves the corresponding file from the `/reports` directory.

---

### 3. Core Module API Documentation

This section details the functions and APIs of the key Python files.

#### 3.1. Business Logic Layer: `analysis_handler.py`
This module is the "process controller" of the system. It orchestrates the entire analysis workflow.

##### Function: `process_uploaded_file(upload_filepath, report_dir, original_filename)`

*   **Purpose:** The sole public interface of the module. It executes the complete workflow from data reading and model invocation to report generation and UI data preparation.
*   **Parameters:**
    *   `upload_filepath` (str): The absolute path to the user-uploaded CSV file saved on the server.
    *   `report_dir` (str): The directory path where the generated CSV reports should be stored.
    *   `original_filename` (str): The original filename provided by the user, used for naming reports.
*   **Returns:** A tuple `(tuple)` containing 5 elements:
    1.  `display_predictions` (list): A list of dictionaries for the full data preview UI.
    2.  `display_alerts` (list): A list of dictionaries for the alert data UI.
    3.  `summary` (dict): A dictionary containing all summary statistics.
    4.  `full_report_filename` (str): The filename of the generated full report.
    5.  `alert_report_filename` (str or None): The filename of the generated alert report, or `None` if no alerts were triggered.
*   **Usage Example (from `app.py`):**
    ```python
    from analysis_handler import process_uploaded_file
    
    # ... inside a Flask route ...
    try:
        (preds, alerts, summary, report_fn, alert_fn) = process_uploaded_file(...)
        return render_template('results.html', predictions=preds, summary=summary, ...)
    except Exception as e:
        return render_template('error.html', error=str(e))
    ```

#### 3.2. AI Model Layer: `models/`

##### File: `models/model_definition.py`
*   **Purpose:** This file **only defines** the neural network architecture of the PyTorch model.
*   **Class: `DDoSDetector(nn.Module)`**: Defines a stacked LSTM network. Its `forward()` method specifies the data path through the network layers.

##### File: `models/prediction.py`
*   **Purpose:** Provides a **clean, efficient, and isolated inference interface**. It loads the model only once at application startup for high performance.
*   **Function: `run_prediction(df_predict)`**
    *   **Purpose:** Receives a prepared DataFrame, performs prediction using the globally loaded model, and returns the results. This is the **only public function** exposed by this module.
    *   **Parameters:**
        *   `df_predict` (pandas.DataFrame): A DataFrame that **must contain exactly** the 10 feature columns required by the model, in the correct order.
    *   **Returns:** A tuple `(tuple)` containing 2 elements:
        1.  `predictions_list` (list): A list of predicted class strings (`'DDoS'` or `'BENIGN'`).
        2.  `probabilities_list` (list): A list of formatted prediction probability strings.
    *   **Usage Example (from `analysis_handler.py`):**
        ```python
        from models.prediction import run_prediction
        
        pred_classes, pred_probs = run_prediction(df_features)
        df['Prediction_Class'] = pred_classes
        ```

---

### 4. Web Routes (API Endpoints)

The application exposes the following endpoints:

#### 4.1. `GET, POST /`
*   **Endpoint:** The root URL of the application.
*   **Methods:** `GET`, `POST`
*   **Description:**
    *   **GET:** Renders the main upload page (`index.html`).
    *   **POST:** Handles the analysis request. It expects a file upload (`multipart/form-data`) and orchestrates the analysis pipeline.
*   **Response:** Renders `results.html` on success or `error.html` on failure.

#### 4.2. `GET /download/<filename>`
*   **Endpoint:** `/download/<filename>`
*   **Method:** `GET`
*   **Description:** Allows the user to download a previously generated report file. It handles both full and alert-only report downloads.
*   **Response:** The requested file from the `/reports` directory, served as an attachment to trigger a browser download.
