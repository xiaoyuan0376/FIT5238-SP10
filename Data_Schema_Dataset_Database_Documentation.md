# Data Schema, Dataset and Database Documentation

## 1. Introduction

This document provides a overview of the data schema, dataset structure, and database used in this project.

## 2. Data Schema

### 2.1 Input Data Schema

The system processes network traffic data in CSV format with the following key features used for DDoS detection:

| Feature Name | Description | Data Type |
|--------------|-------------|-----------|
| Source IP | IP address of the traffic source | String |
| Total Length of Fwd Packets | Total size of forward packets | Numeric |
| Fwd Packet Length Max | Maximum length of forward packets | Numeric |
| Fwd Packet Length Mean | Average length of forward packets | Numeric |
| Bwd Packet Length Min | Minimum length of backward packets | Numeric |
| Fwd IAT Std | Standard deviation of forward inter-arrival times | Numeric |
| Avg Fwd Segment Size | Average size of forward segments | Numeric |
| Subflow Fwd Packets | Number of forward packets in subflow | Numeric |
| Subflow Fwd Bytes | Number of forward bytes in subflow | Numeric |
| Init_Win_bytes_forward | Initial window size for forward traffic | Numeric |
| act_data_pkt_fwd | Number of active forward data packets | Numeric |

Note: The system uses only 10 key features from the original dataset for prediction, focusing on the most relevant network traffic characteristics for DDoS detection.

### 2.2 Output Data Schema

The system generates analysis reports with the following additional fields:

| Feature Name | Description | Data Type |
|--------------|-------------|-----------|
| Prediction_Class | Classification result (DDoS/BENIGN) | String |
| Prediction_Probability | Probability of DDoS classification | Float (0-1) |
| Risk_Score | Risk level assessment | String (Critical/High/Medium/Low) |
| Alert_Triggered | Indicates if alert was triggered | String (YES/NO) |

### 2.3 Risk Assessment Schema

Risk scores are assigned based on prediction probabilities:

- Critical: Probability > 0.95
- High: Probability > 0.8
- Medium: Probability > 0.5
- Low: Probability <= 0.5

Alerts are triggered only for Critical risk scores (probability > 0.95).

## 3. Dataset Information

### 3.1 Dataset Structure

The dataset contains network traffic flow information with over 80 features capturing various aspects of network communication. Each row represents a single network flow with associated metrics.

Key characteristics:
- Format: CSV (Comma-Separated Values)
- Features: Over 80 network traffic attributes
- Sample dataset: `random_test_set_4.csv` with 1000+ flow records
- Size: Variable depending on network traffic volume

### 3.2 Feature Selection

The machine learning model uses a subset of 10 features that are most relevant for DDoS detection:

1. Fwd Packet Length Mean
2. Fwd Packet Length Max
3. Avg Fwd Segment Size
4. Init_Win_bytes_forward
5. Subflow Fwd Bytes
6. Total Length of Fwd Packets
7. act_data_pkt_fwd
8. Bwd Packet Length Min
9. Subflow Fwd Packets
10. Fwd IAT Std

These features were selected based on their relevance to identifying DDoS attack patterns in network traffic.

### 3.3 Data Preprocessing

Before feeding data to the model:
1. Only required columns are extracted from the input CSV
2. Data is converted to appropriate numeric formats
3. Missing or invalid values are handled
4. Data is normalized and formatted for the LSTM model

## 4. Database Design

### 4.1 Firebase Firestore Database

The system uses Firebase Firestore as its primary database for user authentication and management.

#### 4.1.1 Users Collection

Structure:
```
users: collection
  └── user_document: document
      ├── phone: string
      ├── username: string
      ├── password: string
```

Fields:
- `phone`: User's phone number for account identification
- `username`: Unique username for login
- `password`: User's password (Note: In a production environment, this should be hashed)

#### 4.1.2 Database Operations

1. **User Registration**
   - Check if phone number or username already exists
   - Add new user document to the users collection

2. **User Authentication**
   - Query users collection by username or phone number
   - Verify password for authentication
   - Create session for authenticated users

3. **Session Management**
   - Sessions are managed using Flask's session mechanism
   - User ID and username are stored in session upon login
   - Sessions are cleared upon logout

### 4.2 File Storage

The system uses the local file system for temporary storage:

#### 4.2.1 Uploads Directory
- Location: `uploads/`
- Purpose: Temporary storage of uploaded CSV files
- Lifecycle: Files are processed and then retained for potential reuse

#### 4.2.2 Reports Directory
- Location: `reports/`
- Purpose: Storage of generated analysis reports
- Two types of reports:
  1. Full reports with complete analysis
  2. Alert-only reports with critical findings

## 5. Machine Learning Model Data Flow

### 5.1 Data Flow Process

1. **Input**: CSV file with network traffic data
2. **Preprocessing**: Extract required features and format for model input
3. **Prediction**: LSTM model processes data and outputs probabilities
4. **Post-processing**: Convert probabilities to classifications and risk scores
5. **Storage**: Results stored in reports and displayed in UI
6. **Database**: User data stored in Firebase Firestore

### 5.2 Model Input/Output

**Input Shape**: The LSTM model expects input with shape (batch_size, sequence_length, input_dim) where:
- batch_size: 1 (processing one flow at a time)
- sequence_length: 1 (single time step)
- input_dim: 10 (features)

**Output**: A single probability value between 0 and 1 indicating the likelihood of DDoS traffic.

## 6. Reporting Schema

### 6.1 Full Report Structure

Each full report contains:
1. Analysis metadata (timestamp, original filename)
2. Summary statistics (total flows, DDoS flows, benign flows, percentages)
3. Threat intelligence (top attacking IP addresses)
4. Full data log with all original data plus prediction results

### 6.2 Alert Report Structure

Alert reports contain only the subset of traffic classified as "Critical" risk:
- Same data schema as full report but filtered
- Only flows with probability > 0.95
- Alert_Triggered field set to "YES"

## 7. Security Considerations

1. **Data Privacy**: Network traffic data may contain sensitive information and should be handled according to privacy regulations
2. **User Credentials**: User passwords should be properly hashed in production (current implementation stores in plain text for simplicity)
3. **File Uploads**: CSV files should be validated and sanitized to prevent malicious uploads
4. **Access Control**: Reports contain sensitive security information and should be protected with appropriate access controls

## 8. Performance Considerations

1. **Memory Usage**: Large datasets are processed in chunks to manage memory usage
2. **Processing Time**: Prediction time depends on dataset size and hardware capabilities
3. **Storage**: Reports are stored locally and may require periodic cleanup
4. **Scalability**: Firebase Firestore provides good scalability for user data management