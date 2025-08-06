import sys
import os
import unittest
import pandas as pd
import torch

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

# 修复导入问题
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.prediction import run_prediction, MODEL

class TestPrediction(unittest.TestCase):
    """测试预测模块"""
    
    def setUp(self):
        """测试前准备"""
        # 创建测试数据
        self.test_data = pd.DataFrame({
            ' Fwd Packet Length Mean': [10.5, 20.1, 15.7],
            ' Fwd Packet Length Max': [100.0, 200.0, 150.0],
            ' Avg Fwd Segment Size': [50.2, 75.3, 60.1],
            'Init_Win_bytes_forward': [1024.0, 2048.0, 1536.0],
            ' Subflow Fwd Bytes': [512.0, 1024.0, 768.0],
            'Total Length of Fwd Packets': [1000.0, 2000.0, 1500.0],
            ' act_data_pkt_fwd': [5.0, 10.0, 7.0],
            ' Bwd Packet Length Min': [20.0, 30.0, 25.0],
            'Subflow Fwd Packets': [3.0, 6.0, 4.0],
            ' Fwd IAT Std': [1.5, 2.0, 1.8]
        })
        
    def test_model_loading(self):
        """测试模型加载 - 对应文档中的UT-003"""
        # 验证模型是否成功加载
        self.assertIsNotNone(MODEL)
        # 验证模型是DDoSDetector的实例
        self.assertIsInstance(MODEL, torch.nn.Module)
        
    def test_run_prediction(self):
        """测试预测功能 - 对应文档中的UT-004"""
        # 执行预测
        predictions, probabilities = run_prediction(self.test_data)
        
        # 验证返回值类型
        self.assertIsInstance(predictions, list)
        self.assertIsInstance(probabilities, list)
        
        # 验证返回值长度
        self.assertEqual(len(predictions), len(self.test_data))
        self.assertEqual(len(probabilities), len(self.test_data))
        
        # 验证预测结果格式
        for pred in predictions:
            self.assertIn(pred, ["DDoS", "BENIGN"])
            
        # 验证概率结果格式
        for prob in probabilities:
            self.assertIsInstance(prob, str)
            # 检查是否可以转换为浮点数
            prob_val = float(prob)
            self.assertTrue(0 <= prob_val <= 1)

if __name__ == '__main__':
    unittest.main()