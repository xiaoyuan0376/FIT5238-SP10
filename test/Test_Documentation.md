# Test Documentation

## Test Cases

### 1. Unit Tests

#### 1.1 Model Definition Module Tests (models/model_definition.py)

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| UT-001 | LSTM model initialization test | input_dim=10 | Successfully create DDoSDetector instance with 4 LSTM layers + Full-Connected layer | Verify model components (lstm1-4, fc) initialization | ✅ Passed |
| UT-002 | Model forward propagation test | Random tensor (1,1,10) | Single sigmoid output [0,1], no NaN/inf values | Verify forward pass output shape and range | ✅ Passed |

UT-001 and UT-002

![UT-001 and UT-002](https://tuchuang-1318407677.cos.ap-nanjing.myqcloud.com/img/image-20250820111410084.png?imageSlim)

#### 1.2 Prediction Module Tests (models/prediction.py)

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| UT-003 | Model loading test | Pre-trained model file | MODEL global variable loaded as torch.nn.Module | Verify model loading and type validation | ✅ Passed |
| UT-004 | Prediction function test | DataFrame with 10 required features | Lists of predictions ["DDoS"/"BENIGN"] and probabilities [0-1] | Verify run_prediction function return format and content | ✅ Passed |

UT-003 and UT-004  

![image-20250820111817643](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820111817643.png)

#### 1.3 Data Processing Module Tests (analysis_handler.py)

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| UT-005 | Risk scoring mapping test | Probabilities: 0.96, 0.85, 0.6, 0.3, edge cases | Risk levels: Critical(>0.95), High(>0.8), Medium(>0.5), Low(≤0.5) | Verify _map_risk_score function with boundary values and invalid inputs | ✅ Passed |
| UT-006 | File processing function test | CSV file with 3 rows of 10 features | 5-tuple: (predictions, alerts, summary, report_filename, alert_filename) | Verify process_uploaded_file complete workflow | ✅ Passed |

UT-005 and UT-005

![image-20250820111940898](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820111940898.png)

### 2. Integration Tests

#### 2.1 Web Application Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| IT-001 | File upload workflow | CSV file via web interface | Successfully processed with results page render | End-to-end upload → analysis → display | Manual Testing Required |
| IT-002 | Report download functionality | Report filename from /reports/ | CSV file download with correct headers | Test /report/<filename> endpoint | Manual Testing Required |
| IT-003 | Real-time analysis interface | Network data via RealCheck.html | Live analysis results display | Test real-time detection interface | Manual Testing Required |

IT-001

![image-20250820112521517](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820112521517.png)

IT-002

![image-20250820112619890](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820112619890.png)

![image-20250820113041761](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820113041761.png)

IT-003

![image-20250820112650954](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820112650954.png)

#### 2.2 Data Flow Integration Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| IT-004 | Complete analysis pipeline | Full dataset (test sets 1-5 + real data) | Analysis reports in /reports/ directory | Verify uploads → processing → reports generation | ✅ Passed |

### 3. Functional Tests

#### 3.1 Core ML Functionality Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| FT-001 | DDoS detection accuracy test | test_set.csv with ground truth labels | Accuracy ≥70%, proper classification report | Test using sklearn metrics on real dataset | ✅ Passed (≥70% accuracy requirement) |
| FT-002 | Risk scoring validation | Various probability thresholds | Accurate risk level mapping with edge case handling | Test boundary values: 0.95, 0.8, 0.5 thresholds | ✅ Passed |
| FT-003 | Alert generation system | High-risk predictions (Critical/High) | Alert flags triggered for appropriate risk levels | Verify alert_triggered field in results | ✅ Passed |

FT-001 and FT-002

![image-20250820112151176](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820112151176.png)

FT-003

![image-20250820113118447](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820113118447.png)

#### 3.2 System Performance Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| FT-004 | Batch processing performance | Large CSV files (>1000 rows) | Processing completes within reasonable time | Monitor processing time for large datasets | ✅ Passed (2000 rows in 2-3 seconds) |
| FT-005 | Model inference speed | Single prediction requests | Response time <1 second per prediction | Time measurement of prediction calls | ✅ Passed (0.57ms per prediction) |

FT-004

The CSV file with 2000 records was uploaded, and the analysis was completed in just 2-3 seconds

FT-005

![image-20250820113954115](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820113954115.png)

### 4. Data Quality Tests

#### 4.1 Input Validation Tests

| Test Case ID | Test Description | Input | Expected Output | Test Method | Test Result |
|--------------|------------------|-------|-----------------|-------------|-------------|
| DQ-001 | Required feature validation | CSV missing required columns | Graceful error handling with informative messages | Test with incomplete feature sets | ✅ Passed |
| DQ-002 | Data type validation | Invalid data types in CSV | Type conversion or error handling | Test with non-numeric values in numeric columns | ✅ Passed |
| DQ-003 | Data range validation | Out-of-range values | Data normalization or filtering | Test with extreme values | ✅ Passed |

![image-20250820115612289](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820115612289.png)

## Test Execution

### Automated Testing Strategy

| Test Level | Test Files | Execution Method | Status |
|------------|------------|------------------|--------|
| Unit Tests | `test_model_definition.py`, `test_prediction.py`, `test_analysis_handler.py` | Direct Python file execution | ✅ Completed |
| Functional Tests | `test_functional.py` | Direct Python file execution | ✅ Completed |
| Performance Tests | `test_performance.py` | Direct Python file execution | ✅ Completed |
| Data Quality Tests | `test_data_quality.py` | Direct Python file execution | ✅ Completed |
| Integration Tests | Manual web interface testing | Browser end-to-end testing | ✅ Completed |

### Test Data Management

#### Available Test Datasets
- **Primary Test Set**: `test/test_set.csv` - Labeled dataset for accuracy validation
- **Random Test Sets**: `random_test_sets/random_test_set_1-5.csv` - Various traffic patterns
- **Real World Data**: `uploads/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` - Actual DDoS attack data
- **Feature Reference**: `uploads/top_10_features.csv` - Required feature specifications

#### Required Features for Testing
```
Required Model Input Features (10):
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
```

### Performance Metrics

#### Test Coverage Metrics
- **Unit Test Coverage**: 100% (6/6 core functions tested)
- **Integration Test Coverage**: 100% (4/4 integration paths tested)
- **Functional Test Coverage**: 100% (5/5 functional requirements tested)
- **Data Quality Test Coverage**: 100% (3/3 data quality tests implemented)

#### Quality Metrics
- **Test Pass Rate**: 100% (All automated tests passing)
- **Model Accuracy**: 86.8% 
- **DDoS Detection Recall**: 98% (Excellent attack detection capability)
- **BENIGN Precision**: 97% (Low false positive rate)
- **Single Prediction Speed**: 0.57ms 
- **Batch Processing Performance**: 0.49-0.60ms per row (2000 rows in 2-3 seconds)
- **Memory Efficiency**: Only 0.08MB increase per 1000 records

#### Current Test Results Summary
```
✅ Automated Tests Passing: 13/13
✅ Manual Integration Tests Passed: 3/3  
✅ Performance Tests Passed: 2/2
✅ Data Quality Tests Passed: 5/5
🎉 Overall Test Pass Rate: 100%
```

## Test Environment Setup

### Recommended Test Execution Method
```bash
# Switch to test directory
cd test

# Run all tests in order (recommended method)
# 1. Unit Tests
python test_model_definition.py      # UT-001, UT-002
python test_prediction.py            # UT-003, UT-004  
python test_analysis_handler.py      # UT-005, UT-006

# 2. Functional Tests
python test_functional.py            # FT-001, FT-002, FT-003

# 3. Performance Tests
python test_performance.py           # FT-005 (FT-004 via manual web interface testing)

# 4. Data Quality Tests
python test_data_quality.py          # DQ-001, DQ-002, DQ-003
```

### Alternative Execution Methods
```bash
# Using unittest module (if path configuration is correct)
python -m unittest discover . -p "test_*.py" -v

# Generate test coverage report (if coverage.py available)
coverage run -m unittest discover . -p "test_*.py"
coverage report -m
coverage html  # Generate HTML report
```

### Integration Test Execution Steps
```bash
# Start web application
cd ..  # Return to project root directory
python app.py

# Then perform the following tests in browser:
# IT-001: Visit homepage, test CSV file upload
# IT-002: Test report download functionality
# IT-003: Test RealCheck.html real-time analysis interface
```

## Test Case to Implementation Mapping

| Test Case ID | Test Description | Implementation File | Execution Method | Test Status |
|--------------|------------------|-------------------|------------------|-------------|
| UT-001 | Model initialization | `test_model_definition.py` | `python test_model_definition.py` | ✅ Passed |
| UT-002 | Forward propagation | `test_model_definition.py` | `python test_model_definition.py` | ✅ Passed |
| UT-003 | Model loading | `test_prediction.py` | `python test_prediction.py` | ✅ Passed |
| UT-004 | Prediction function | `test_prediction.py` | `python test_prediction.py` | ✅ Passed |
| UT-005 | Risk scoring | `test_analysis_handler.py` | `python test_analysis_handler.py` | ✅ Passed |
| UT-006 | File processing | `test_analysis_handler.py` | `python test_analysis_handler.py` | ✅ Passed |
| FT-001 | DDoS accuracy test | `test_functional.py` | `python test_functional.py` | ✅ Passed |
| FT-002 | Risk scoring validation | `test_functional.py` | `python test_functional.py` | ✅ Passed |
| FT-003 | Alert generation system | Manual web interface testing | Browser testing | ✅ Passed |
| FT-004 | Batch processing performance | Manual web interface large file testing | Upload large CSV file | ✅ Passed |
| FT-005 | Inference speed | `test_performance.py` | `python test_performance.py` | ✅ Passed |
| IT-001 | File upload workflow | Manual web interface testing | Browser end-to-end testing | ✅ Passed |
| IT-002 | Report download functionality | Manual web interface testing | Browser download testing | ✅ Passed |
| IT-003 | Real-time analysis interface | Manual web interface testing | RealCheck.html testing | ✅ Passed |
| IT-004 | Complete analysis pipeline | Automated integration testing | File processing workflow | ✅ Passed |
| DQ-001 | Required feature validation | `test_data_quality.py` | `python test_data_quality.py` | ✅ Passed |
| DQ-002 | Data type validation | `test_data_quality.py` | `python test_data_quality.py` | ✅ Passed |
| DQ-003 | Data range validation | `test_data_quality.py` | `python test_data_quality.py` | ✅ Passed |

