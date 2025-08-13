import sys
import os
import unittest
import torch

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

from model_definition import DDoSDetector

class TestDDoSDetector(unittest.TestCase):
    """测试DDoSDetector模型定义"""
    
    def setUp(self):
        """测试前准备"""
        self.input_dim = 10
        self.model = DDoSDetector(input_dim=self.input_dim)
        
    def test_model_initialization(self):
        """测试模型初始化 - 对应文档中的UT-001"""
        # 验证模型是否成功创建
        self.assertIsInstance(self.model, DDoSDetector)
        # 验证LSTM层是否正确初始化
        self.assertIsNotNone(self.model.lstm1)
        self.assertIsNotNone(self.model.lstm2)
        self.assertIsNotNone(self.model.lstm3)
        self.assertIsNotNone(self.model.lstm4)
        # 验证全连接层是否正确初始化
        self.assertIsNotNone(self.model.fc)
        
    def test_forward_pass(self):
        """测试模型前向传播 - 对应文档中的UT-002"""
        # 创建测试输入数据 (batch_size=1, seq_len=1, input_dim=10)
        test_input = torch.randn(1, 1, self.input_dim)
        
        # 执行前向传播
        with torch.no_grad():
            output = self.model(test_input)
            
        # 验证输出形状是否正确 (batch_size=1, output_dim=1)
        self.assertEqual(output.shape, (1, 1))
        
        # 验证输出值是否在合理范围内 (0-1之间，因为使用了sigmoid激活函数)
        self.assertTrue(torch.all(output >= 0))
        self.assertTrue(torch.all(output <= 1))
        
        # 验证输出值是确定的数值（不是NaN或inf）
        self.assertFalse(torch.isnan(output).any())
        self.assertFalse(torch.isinf(output).any())

if __name__ == '__main__':
    unittest.main()