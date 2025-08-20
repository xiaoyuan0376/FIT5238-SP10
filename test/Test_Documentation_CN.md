# 测试文档

## 测试用例

### 1. 单元测试

#### 1.1 模型定义模块测试 (models/model_definition.py)

| 测试用例ID | 测试描述 | 输入 | 预期输出 | 测试方法 | 测试结果 |
|-----------|---------|------|----------|----------|----------|
| UT-001 | LSTM模型初始化测试 | input_dim=10 | 成功创建包含4个LSTM层+全连接层的DDoSDetector实例 | 验证模型组件(lstm1-4, fc)初始化 | ✅ 通过 |
| UT-002 | 模型前向传播测试 | 随机张量(1,1,10) | 单个sigmoid输出[0,1]，无NaN/inf值 | 验证前向传播输出形状和范围 | ✅ 通过 |

![UT-001](https://tuchuang-1318407677.cos.ap-nanjing.myqcloud.com/img/image-20250820111410084.png?imageSlim)

#### 1.2 预测模块测试 (models/prediction.py)

| 测试用例ID | 测试描述 | 输入 | 预期输出 | 测试方法 | 测试结果 |
|-----------|---------|------|----------|----------|----------|
| UT-003 | 模型加载测试 | 预训练模型文件 | MODEL全局变量加载为torch.nn.Module | 验证模型加载和类型验证 | ✅ 通过 |
| UT-004 | 预测功能测试 | 包含10个必需特征的DataFrame | 预测结果列表["DDoS"/"BENIGN"]和概率列表[0-1] | 验证run_prediction函数返回格式和内容 | ✅ 通过 |

![image-20250820111817643](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820111817643.png)

#### 1.3 数据处理模块测试 (analysis_handler.py)

| 测试用例ID | 测试描述 | 输入 | 预期输出 | 测试方法 | 测试结果 |
|-----------|---------|------|----------|----------|----------|
| UT-005 | 风险评分映射测试 | 概率值: 0.96, 0.85, 0.6, 0.3, 边界情况 | 风险等级: Critical(>0.95), High(>0.8), Medium(>0.5), Low(≤0.5) | 使用边界值和无效输入验证_map_risk_score函数 | ✅ 通过 |
| UT-006 | 文件处理功能测试 | 包含3行10个特征的CSV文件 | 5元组: (预测结果, 警报, 摘要, 报告文件名, 警报文件名) | 验证process_uploaded_file完整工作流程 | ✅ 通过 |

![image-20250820111940898](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820111940898.png)

### 2. 集成测试

#### 2.1 Web应用程序测试

| 测试用例ID | 测试描述 | 输入 | 预期输出 | 测试方法 | 测试结果 |
|-----------|---------|------|----------|----------|----------|
| IT-001 | 文件上传工作流 | 通过Web界面上传CSV文件 | 成功处理并渲染结果页面 | 端到端测试：上传 → 分析 → 显示 | ✅ 通过 |
| IT-002 | 报告下载功能 | 来自/reports/的报告文件名 | CSV文件下载，包含正确标题 | 测试/report/<filename>端点 | ✅ 通过 |
| IT-003 | 实时分析界面 | 通过RealCheck.html的网络数据 | 实时分析结果显示 | 测试实时检测界面 | ✅ 通过 |

IT-001

![image-20250820112521517](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820112521517.png)

IT-002

![image-20250820112619890](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820112619890.png)

![image-20250820113041761](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820113041761.png)

IT-003

![image-20250820112650954](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820112650954.png)

#### 2.2 数据流集成测试

| 测试用例ID | 测试描述 | 输入 | 预期输出 | 测试方法 | 测试结果 |
|-----------|---------|------|----------|----------|----------|
| IT-004 | 完整分析管道 | 完整数据集(测试集1-5 + 实际数据) | /reports/目录中的分析报告 | 验证上传 → 处理 → 报告生成 | ✅ 通过 |

### 3. 功能测试

#### 3.1 核心ML功能测试

| 测试用例ID | 测试描述 | 输入 | 预期输出 | 测试方法 | 测试结果 |
|-----------|---------|------|----------|----------|----------|
| FT-001 | DDoS检测准确率测试 | 带有真实标签的test_set.csv | 准确率≥70%，适当的分类报告 | 使用sklearn指标在真实数据集上测试 | ✅ 通过 |
| FT-002 | 风险评分验证 | 各种概率阈值 | 准确的风险等级映射和边界情况处理 | 测试边界值: 0.95, 0.8, 0.5阈值 | ✅ 通过 |
| FT-003 | 警报生成系统 | 高风险预测(Critical/High) | 为适当的风险等级触发警报标志 | 验证结果中的alert_triggered字段 | ✅ 通过 |

FT-001 and FT-002

![image-20250820112151176](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820112151176.png)

FT-003

![image-20250820113118447](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820113118447.png)

#### 3.2 系统性能测试

| 测试用例ID | 测试描述 | 输入 | 预期输出 | 测试方法 | 测试结果 |
|-----------|---------|------|----------|----------|----------|
| FT-004 | 批处理性能 | 大型CSV文件(>1000行) | 在合理时间内完成处理 | 监控大型数据集的处理时间 | ✅ 通过(2000行2-3秒) |
| FT-005 | 模型推理速度 | 单个预测请求 | 每个预测响应时间<1秒 | 测量预测调用的时间 | ✅ 通过(0.57毫秒/预测) |

FT-004

The CSV file with 2000 records was uploaded, and the analysis was completed in just 2-3 seconds

FT-005

![image-20250820113954115](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820113954115.png)

### 4. 数据质量测试

#### 4.1 输入验证测试

| 测试用例ID | 测试描述 | 输入 | 预期输出 | 测试方法 | 测试结果 |
|-----------|---------|------|----------|----------|----------|
| DQ-001 | 必需特征验证 | 缺少必需列的CSV | 优雅的错误处理和信息提示 | 使用不完整特征集测试 | ✅ 通过 |
| DQ-002 | 数据类型验证 | CSV中的无效数据类型 | 类型转换或错误处理 | 在数值列中测试非数值值 | ✅ 通过 |
| DQ-003 | 数据范围验证 | 超出范围的值 | 数据标准化或过滤 | 测试极端值 | ✅ 通过 |

![image-20250820115612289](C:\Users\Sean\AppData\Roaming\Typora\typora-user-images\image-20250820115612289.png)

## 测试执行

### 自动化测试策略

| 测试级别 | 测试文件 | 执行方法 | 状态 |
|---------|----------|----------|------|
| 单元测试 | `test_model_definition.py`, `test_prediction.py`, `test_analysis_handler.py` | 直接运行Python文件 | ✅ 完成 |
| 功能测试 | `test_functional.py` | 直接运行Python文件 | ✅ 完成 |
| 性能测试 | `test_performance.py` | 直接运行Python文件 | ✅ 完成 |
| 数据质量测试 | `test_data_quality.py` | 直接运行Python文件 | ✅ 完成 |
| 集成测试 | 手动Web界面测试 | 浏览器端到端测试 | ✅ 完成 |

### 测试数据管理

#### 可用测试数据集
- **主要测试集**: `test/test_set.csv` - 用于准确率验证的标注数据集
- **随机测试集**: `random_test_sets/random_test_set_1-5.csv` - 各种流量模式
- **真实世界数据**: `uploads/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` - 实际DDoS攻击数据
- **特征参考**: `uploads/top_10_features.csv` - 必需特征规范

#### 测试所需特征
```
必需模型输入特征(10个):
1. Fwd Packet Length Mean        (前向数据包长度均值)
2. Fwd Packet Length Max         (前向数据包长度最大值)
3. Avg Fwd Segment Size          (平均前向段大小)
4. Init_Win_bytes_forward        (前向初始窗口字节数)
5. Subflow Fwd Bytes             (子流前向字节数)
6. Total Length of Fwd Packets   (前向数据包总长度)
7. act_data_pkt_fwd              (前向活动数据包数)
8. Bwd Packet Length Min         (后向数据包长度最小值)
9. Subflow Fwd Packets           (子流前向数据包数)
10. Fwd IAT Std                  (前向到达间隔时间标准差)
```

### 性能指标

#### 测试覆盖率指标
- **单元测试覆盖率**: 100% (6/6核心功能已测试)
- **集成测试覆盖率**: 100% (4/4集成路径已测试)
- **功能测试覆盖率**: 100% (5/5功能需求已测试)
- **数据质量测试覆盖率**: 100% (3/3数据质量测试已实现)

#### 质量指标
- **测试通过率**: 100% (所有自动化测试通过)
- **模型准确率**: 86.8% 
- **DDoS检测召回率**: 98% (优秀的攻击检测能力)
- **BENIGN精确率**: 97% (低误报率)
- **单次预测速度**: 0.57毫秒 
- **批处理性能**: 0.49-0.60毫秒/行 (2000行数据2-3秒完成)
- **内存效率**: 每1000条记录仅增长0.08MB

#### 当前测试结果摘要
```
✅ 自动化测试通过: 13/13
✅ 手动集成测试通过: 3/3  
✅ 性能测试通过: 2/2
✅ 数据质量测试通过: 5/5
🎉 总体测试通过率: 100%
```

## 测试环境设置

### 推荐测试执行方法
```bash
# 切换到test目录
cd test

# 按顺序运行所有测试（推荐方法）
# 1. 单元测试
python test_model_definition.py      # UT-001, UT-002
python test_prediction.py            # UT-003, UT-004  
python test_analysis_handler.py      # UT-005, UT-006

# 2. 功能测试
python test_functional.py            # FT-001, FT-002, FT-003

# 3. 性能测试
python test_performance.py           # FT-005 (FT-004通过Web界面手动测试)

# 4. 数据质量测试
python test_data_quality.py          # DQ-001, DQ-002, DQ-003
```

### 替代执行方法
```bash
# 使用unittest模块（如果路径设置正确）
python -m unittest discover . -p "test_*.py" -v

# 生成测试覆盖率报告(如果安装了coverage.py)
coverage run -m unittest discover . -p "test_*.py"
coverage report -m
coverage html  # 生成HTML报告
```

### 集成测试执行步骤
```bash
# 启动Web应用
cd ..  # 回到项目根目录
python app.py

# 然后在浏览器中进行以下测试：
# IT-001: 访问主页，上传CSV文件测试
# IT-002: 测试报告下载功能
# IT-003: 测试RealCheck.html实时分析界面
```

## 测试用例到实现映射

| 测试用例ID | 测试描述 | 实现文件 | 执行方法 | 测试状态 |
|-----------|---------|----------|----------|----------|
| UT-001 | 模型初始化 | `test_model_definition.py` | `python test_model_definition.py` | ✅ 通过 |
| UT-002 | 前向传播 | `test_model_definition.py` | `python test_model_definition.py` | ✅ 通过 |
| UT-003 | 模型加载 | `test_prediction.py` | `python test_prediction.py` | ✅ 通过 |
| UT-004 | 预测功能 | `test_prediction.py` | `python test_prediction.py` | ✅ 通过 |
| UT-005 | 风险评分 | `test_analysis_handler.py` | `python test_analysis_handler.py` | ✅ 通过 |
| UT-006 | 文件处理 | `test_analysis_handler.py` | `python test_analysis_handler.py` | ✅ 通过 |
| FT-001 | DDoS准确率测试 | `test_functional.py` | `python test_functional.py` | ✅ 通过 |
| FT-002 | 风险评分验证 | `test_functional.py` | `python test_functional.py` | ✅ 通过 |
| FT-003 | 警报生成系统 | 手动Web界面测试 | 浏览器测试 | ✅ 通过 |
| FT-004 | 批处理性能 | 手动Web界面大文件测试 | 上传大CSV文件 | ✅ 通过 |
| FT-005 | 推理速度 | `test_performance.py` | `python test_performance.py` | ✅ 通过 |
| IT-001 | 文件上传工作流 | 手动Web界面测试 | 浏览器端到端测试 | ✅ 通过 |
| IT-002 | 报告下载功能 | 手动Web界面测试 | 浏览器下载测试 | ✅ 通过 |
| IT-003 | 实时分析界面 | 手动Web界面测试 | RealCheck.html测试 | ✅ 通过 |
| IT-004 | 完整分析管道 | 自动化集成测试 | 文件处理工作流 | ✅ 通过 |
| DQ-001 | 必需特征验证 | `test_data_quality.py` | `python test_data_quality.py` | ✅ 通过 |
| DQ-002 | 数据类型验证 | `test_data_quality.py` | `python test_data_quality.py` | ✅ 通过 |
| DQ-003 | 数据范围验证 | `test_data_quality.py` | `python test_data_quality.py` | ✅ 通过 |