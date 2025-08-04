# DDoS流量检测系统

## 项目概述

本项目是一个基于机器学习和深度学习的DDoS攻击检测系统。该系统能够分析网络流量数据，识别影响DDoS攻击的关键特征，并使用训练好的模型对新的网络流量进行预测分析。

目标用户: 数据科学家、研究人员、网络安全专业人员。

核心功能:
- 特征分析: 通过机器学习算法分析特征对DDoS检测结果的影响程度
- 模型训练: 使用真实网络流量数据训练深度学习模型
- 模型预测: 利用训练好的模型对新数据进行DDoS攻击预测
- Web展示: 提供友好的Web界面用于交互式分析和结果展示

## 技术架构

### 整体架构
```
┌─────────────────┐
│   Web浏览器      │
└─────────┬───────┘
          │ HTTP请求
┌─────────▼───────┐
│   Flask应用     │
│  (webapp.py)    │
└───┬─────────┬───┘
    │         │
    │调用分析  │调用预测
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ 数据分析 │ │ 深度学习模型  │
│ 模块     │ │ 模块         │
└─────────┘ └──────────────┘
```

### 技术栈
- 后端框架: Python Flask
- 数据处理: pandas, numpy
- 机器学习: scikit-learn
- 深度学习: PyTorch
- 数据可视化: matplotlib, seaborn
- 前端模板: Jinja2

## 模块说明

### 1. 数据分析模块 (analysis/)
- **initAna.py**: 数据预处理、特征分析和可视化功能
  - `load_and_preprocess_data()`: 加载并清洗CSV数据
  - `feature_analysis()`: 使用随机森林算法进行特征重要性分析
  - `visualize_and_save()`: 生成特征重要性图表并保存结果

### 2. 深度学习模型模块 (models/)
- **model.py**: 定义基于LSTM的DDoSDetector模型
  - 多层LSTM架构用于序列数据处理
  - 包含Dropout层防止过拟合

- **train.py**: 模型训练脚本
  - 数据预处理和加载
  - 模型训练和验证
  - 模型保存为.pth文件

- **predict.py**: 独立预测脚本
  - 加载训练好的模型
  - 对单条数据进行预测分析

- **predict_utils.py**: Web应用集成的预测功能
  - `predict_ddos_traffic()`: 为Web应用提供预测接口

- **ddos_detection_model.pth**: 训练好的模型参数文件

### 3. Web应用模块 (web/)
- **webapp.py**: Flask主应用文件
  - 文件上传处理
  - 数据分析流程控制
  - 结果展示和下载功能

- **templates/**: HTML模板文件
  - `index.html`: 文件上传页面
  - `analyze.html`: 分析处理页面
  - `results.html`: 结果展示页面

## 工作流程

### 1. 数据处理流程
1. 用户上传CSV格式的网络流量数据文件
2. 系统加载并预处理数据（清洗、特征选择、标签转换）
3. 使用随机森林算法分析特征重要性
4. 生成特征重要性可视化图表

### 2. 预测分析流程
1. 从预处理后的数据中抽取样本
2. 使用训练好的LSTM模型进行DDoS攻击预测
3. 对比预测结果与实际标签
4. 统计预测准确率

### 3. 结果展示流程
1. 展示特征重要性排行榜（Top 10）
2. 显示预测统计信息（DDoS vs 正常流量）
3. 提供图表可视化展示

## 目录结构

```
project/
├── analysis/           # 数据分析模块
│   └── initAna.py     # 数据预处理和特征分析
├── models/            # 深度学习模型模块
│   ├── model.py       # 模型定义
│   ├── train.py       # 模型训练
│   ├── predict.py     # 独立预测脚本
│   ├── predict_utils.py # Web集成预测功能
│   └── ddos_detection_model.pth # 训练好的模型参数
├── web/               # Web应用模块
│   ├── webapp.py      # Flask主应用
│   └── templates/     # HTML模板
├── uploads/           # 上传文件存储目录
├── results/           # 分析结果存储目录
├── data/              # 示例数据目录
├── requirements.txt   # 项目依赖
└── readme.md         # 项目说明文档
```

## 部署和运行

### 环境要求
- Python 3.x
- 依赖库: flask, torch, pandas, numpy, scikit-learn, matplotlib, seaborn

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行Web应用
```bash
python web/webapp.py
```

访问 http://localhost:5000 查看应用

### 独立脚本使用
```bash
# 模型训练
python models/train.py

# 独立预测
python models/predict.py
```

## 设计特点

### 模块化设计
- 各功能模块职责明确，便于维护和扩展
- 数据处理、模型训练、预测分析和Web展示等功能相互独立

### 双模型策略
- 使用随机森林进行特征分析，提供可解释性
- 使用LSTM深度学习模型进行预测，提高准确性

### 路径管理
- 使用绝对路径确保在不同环境下正常运行
- 避免因工作目录变化导致的文件访问问题

### 错误处理
- 包含完善的异常处理机制
- 提供详细的错误信息便于调试