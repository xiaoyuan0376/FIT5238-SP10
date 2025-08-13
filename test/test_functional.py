import sys
import os
import unittest
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

# Add the project root directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.prediction import run_prediction

class TestFunctional(unittest.TestCase):
    """功能测试"""
    
    def setUp(self):
        """测试前准备"""
        # 读取测试数据集
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'test_set.csv')
        self.test_data = pd.read_csv(self.test_file_path)
        
        # 定义需要的特征列
        self.required_columns = [
            " Fwd Packet Length Mean", " Fwd Packet Length Max", " Avg Fwd Segment Size",
            "Init_Win_bytes_forward", " Subflow Fwd Bytes", "Total Length of Fwd Packets",
            " act_data_pkt_fwd", " Bwd Packet Length Min", "Subflow Fwd Packets",
            " Fwd IAT Std"
        ]
        
    def test_ddos_detection_accuracy(self):
        """测试DDoS检测准确性 - 对应文档中的FT-001"""
        # 选择需要的特征列和标签列
        try:
            df_features = self.test_data[self.required_columns].copy()
            true_labels = self.test_data[' Label'].copy()
        except KeyError as e:
            self.fail(f"测试数据缺少必要的列: {e}")
            
        # 运行预测
        predicted_classes, probabilities = run_prediction(df_features)
        
        # 验证返回值
        self.assertIsInstance(predicted_classes, list)
        self.assertIsInstance(probabilities, list)
        self.assertEqual(len(predicted_classes), len(true_labels))
        self.assertEqual(len(probabilities), len(true_labels))
        
        # 计算准确率
        accuracy = accuracy_score(true_labels, predicted_classes)
        
        # 验证准确率在合理范围内 (假设应该至少有70%的准确率)
        self.assertGreaterEqual(accuracy, 0.7, 
            f"模型准确率低于预期: {accuracy:.4f}. 详细分类报告:\n{classification_report(true_labels, predicted_classes)}")
        
        # 验证预测结果格式
        for pred in predicted_classes:
            self.assertIn(pred, ["DDoS", "BENIGN"], f"预测结果包含无效类别: {pred}")
            
        for prob in probabilities:
            self.assertIsInstance(prob, str)
            prob_val = float(prob)
            self.assertTrue(0 <= prob_val <= 1, f"概率值超出范围: {prob_val}")
            
        print(f"测试数据量: {len(true_labels)}")
        print(f"准确率: {accuracy:.4f}")
        print("分类报告:")
        print(classification_report(true_labels, predicted_classes))
        
    def test_risk_scoring_logic(self):
        """测试风险评分逻辑 - 对应文档中的FT-002"""
        # 从analysis_handler导入风险评分函数
        from analysis_handler import _map_risk_score
        
        # 测试关键风险阈值
        test_cases = [
            (0.96, "Critical"),
            (0.85, "High"),
            (0.60, "Medium"),
            (0.30, "Low"),
            (0.95, "High"),    # 边界测试
            (0.80, "Medium"),  # 边界测试
            (0.50, "Low"),     # 边界测试
        ]
        
        for probability, expected_risk in test_cases:
            with self.subTest(probability=probability):
                actual_risk = _map_risk_score(probability)
                self.assertEqual(actual_risk, expected_risk, 
                    f"风险评分映射错误: 概率{probability}应该映射到{expected_risk}，但得到{actual_risk}")

if __name__ == '__main__':
    unittest.main()