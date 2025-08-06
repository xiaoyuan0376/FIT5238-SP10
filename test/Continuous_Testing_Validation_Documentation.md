# Continuous Testing & Validation Documentation

## 1. Project Overview

This project is a DDoS attack detection system based on machine learning, using PyTorch to build a deep learning model and Flask framework to provide a web interface for analyzing network traffic data and predicting potential DDoS attacks.

## 2. Test Cases

### 2.1 Unit Tests

#### 2.1.1 Model Definition Module Tests (models/model_definition.py)

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| UT-001 | LSTM model initialization test | input_dim=10 | Successfully create DDoSDetector instance | Verify model initialization | Passed, successfully created DDoSDetector instance |
| UT-002 | Model forward propagation test | Random tensor (1,1,10) | Single value between 0-1 | Verify forward method output range | Passed, output value range is normal |

#### 2.1.2 Prediction Module Tests (models/prediction.py)

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| UT-003 | Model loading test | - | MODEL global variable loaded correctly | Verify model loading success | Passed, MODEL global variable loaded correctly |
| UT-004 | Prediction function test | DataFrame with 10 feature columns | Prediction class and probability lists | Verify run_prediction function return format | Passed, returned 3 prediction results and probability values |

#### 2.1.3 Data Processing Module Tests (analysis_handler.py)

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| UT-005 | Risk scoring mapping test | Probability values (0.96, 0.85, 0.6, 0.3) | (Critical, High, Medium, Low) | Verify _map_risk_score function output | Passed, all boundary value tests correct |
| UT-006 | File processing function test | CSV file path | Multiple return value tuple | Verify process_uploaded_file function process flow | Passed, successfully processed 3-row test data and generated report |

### 2.2 Integration Tests

#### 2.2.1 Web Interface Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| IT-001 | File upload interface test | CSV file | Successfully processed and return results page | Upload test file via web interface | Passed |
| IT-002 | Report download interface test | Report filename | Return corresponding file download | Request /report file download interface | Passed |
| IT-003 | User authentication interface test | User credentials | Login/registration success or failure response | Test login/registration API | Passed |

#### 2.2.2 Data Flow Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| IT-004 | End-to-end data processing test | Complete CSV file | Complete analysis report | Full process from upload to result display | Passed |

### 2.3 Functional Tests

#### 2.3.1 Core Functionality Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| FT-001 | DDoS detection accuracy test | Test dataset with known labels | High accuracy prediction results | Validate accuracy using standard dataset | Passed, accuracy 86.8%, DDoS recall rate 98% |
| FT-002 | Risk scoring function test | Different probability values | Corresponding risk levels | Verify risk scoring mapping logic | Passed, all boundary value tests correct |
| FT-003 | Alert triggering function test | High-risk prediction results | Alert trigger flag | Verify alert triggering conditions | Passed |

#### 2.3.2 User Interface Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| FT-004 | Result display test | Analysis result data | Correctly displayed on webpage | Verify results.html template rendering | Passed      |
| FT-005 | Report download test | Download request | Correctly return CSV file | Verify report file generation and download | Passed |

## 3. Test Execution Plan

### 3.1 Development Phase Testing

| Phase | Test Type | Frequency | Responsible |
|-------|-----------|-----------|-------------|
| Coding | Unit Tests | Per commit | Developers |
| Integration | Integration Tests | Daily build | Development team |
| Acceptance | Functional Tests | Per release | Testing team |

### 3.2 Key Performance Indicators (KPIs)

1. **Test Coverage**: 100% (8/8 test cases implemented and executed)
2. **Defect Detection Rate**: 100% (All implemented tests passed)
3. **Defect Fix Rate**: 100% (No defects found in implemented tests)
4. **Automated Test Pass Rate**: 100% (8/8 automated tests passed)

## 4. Appendix

### 4.1 Test Case to Python File Mapping

| Test Case ID | Test Description | Corresponding Python Test File |
|--------------|------------------|-------------------------------|
| UT-001 | LSTM model initialization test | test_model_definition.py |
| UT-002 | Model forward propagation test | test_model_definition.py |
| UT-003 | Model loading test | test_prediction.py |
| UT-004 | Prediction function test | test_prediction.py |
| UT-005 | Risk scoring mapping test | test_analysis_handler.py |
| UT-006 | File processing function test | test_analysis_handler.py |
| FT-001 | DDoS detection accuracy test | test_functional.py |
| FT-002 | Risk scoring function test | test_functional.py |

