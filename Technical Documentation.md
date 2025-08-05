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

#### 3.3. Main Application and Authentication: app.py

app.py is the core of the Flask application, handling not only web request routing but also integrated user authentication and session management.

- **Core Responsibilities:**
  - **User Authentication:** Handles user registration, login, and logout logic through integration with **Google Firebase Firestore**.
  - **Session Management:** Leverages Flask's session object to track user status after login and protect endpoints requiring authentication.
  - **Request Routing:** Defines all web endpoints (see Section 4) and dispatches requests to the appropriate processing logic (e.g., file uploads to analysis_handler).
  - **Serving Static Files and Templates:** Renders HTML pages and serves static assets such as CSS and JS.
- **Firebase Integration:**
  - Initializes the Firebase Admin SDK using serviceAccountKey.json when the application starts.
  - All user data (username, phone number, password) is stored in a Firestore collection named users.
  - When registering, we will check if the phone number or username already exists to ensure uniqueness.

---

* ### 4. Web Routing (API Endpoints)

  The application provides the following API endpoints, divided into two parts: user authentication and core analytics.

  #### 4.1. Authentication Endpoints

  These endpoints together form the complete user authentication process.

  **GET /**

  - **Purpose:** Display the main login/registration page (login_register.html). This is the entry point for all users.
  - **Response:** The rendered HTML page.

  **POST     /api/register**

  - **Purpose:** Handle new user registration requests.
  - **Request Body:** application/json, containing phone number, username, and password.
  - **Response:**
    - registerSuccess (status code 200): User creation successful.
    - registerFailed (status code 200): Phone number or username already exists.
    - Data not full (status code 400): Request data is incomplete.


  **POST     /api/login**

  - **Purpose:** Handle user login requests.
  - **Request Body:** application/x-www-form-urlencoded, containing the IDAccount (can be a username or phone number) and password.
  - **Response:**
    - main (status code 200): Login successful. The server will set up a user session, and the client should redirect to /upload.
    - login failure... (status code 200): Incorrect credentials.
    - data not full (status code 400): The request data is incomplete.


  **GET     /api/logout**

  - **Purpose:** Clears the current user's session and logs out.
  - **Response:** Redirects to the root URL / (login page).

  #### 4.2. Core Functionality Endpoints

  These endpoints are the main analysis functions of the system.

  **GET, POST /upload**

  - **Purpose:**
    - **GET:** Displays the file upload page (index.html), which is the main interface for DDoS analysis.
    - **POST:** Processes the uploaded CSV file for analysis. This is the core endpoint that triggers the entire analysis process.

  - **Request Body (POST):** multipart/form-data, must contain a file part named file.
  - **Response:**
    - **Success:** Renders the results.html page containing the analysis results, summary, and download link.
    - **Failure:** If the file is invalid, there was an error processing, or no file was selected, redirects back to the upload page and displays the error via a flash message, or renders the error.html page with the specific exception.


  **GET /download/<filename>**
  - **Purpose:** Allows the user to download a previously generated report file.
  - **URL Parameters:** filename (str) - The report file name provided in the results.html page.
  - **Response:** Finds the corresponding file from the /reports directory and serves it to the browser as an attachment for download.
