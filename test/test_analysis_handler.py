import sys
import os
import unittest
import tempfile
import pandas as pd

# Add the project root directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from analysis_handler import _map_risk_score, process_uploaded_file

class TestAnalysisHandler(unittest.TestCase):
    """测试数据分析处理模块"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录用于测试
        self.test_dir = tempfile.mkdtemp()
        self.test_csv_path = os.path.join(self.test_dir, 'test_data.csv')
        self.reports_dir = os.path.join(self.test_dir, 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # 创建测试数据
        test_data = pd.DataFrame({
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
        
        # 保存测试数据到CSV文件
        test_data.to_csv(self.test_csv_path, index=False)
        
    def test_map_risk_score(self):
        """测试风险评分映射 - 对应文档中的UT-005"""
        # 测试 Critical 风险等级 (prob > 0.95)
        self.assertEqual(_map_risk_score(0.96), "Critical")
        self.assertEqual(_map_risk_score(0.99), "Critical")
        self.assertEqual(_map_risk_score(1.0), "Critical")
        
        # 测试 High 风险等级 (prob > 0.8)
        self.assertEqual(_map_risk_score(0.85), "High")
        self.assertEqual(_map_risk_score(0.9), "High")
        self.assertEqual(_map_risk_score(0.95), "High")  # 边界值测试
        
        # 测试 Medium 风险等级 (prob > 0.5)
        self.assertEqual(_map_risk_score(0.6), "Medium")
        self.assertEqual(_map_risk_score(0.75), "Medium")
        self.assertEqual(_map_risk_score(0.8), "Medium")  # 边界值测试
        
        # 测试 Low 风险等级 (prob <= 0.5)
        self.assertEqual(_map_risk_score(0.3), "Low")
        self.assertEqual(_map_risk_score(0.5), "Low")  # 边界值测试
        self.assertEqual(_map_risk_score(0.0), "Low")
        
        # 测试无效输入
        self.assertEqual(_map_risk_score("invalid"), "Unknown")
        self.assertEqual(_map_risk_score(None), "Unknown")
        self.assertEqual(_map_risk_score(-1), "Low")  # 负数测试

    def test_process_uploaded_file(self):
        """测试文件处理功能 - 对应文档中的UT-006"""
        # 执行文件处理
        try:
            result = process_uploaded_file(
                upload_filepath=self.test_csv_path,
                report_dir=self.reports_dir,
                original_filename='test_data.csv'
            )
            
            # 验证返回值类型
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 5)
            
            # 验证返回的各个部分
            display_predictions, display_alerts, summary, full_report_filename, alert_report_filename = result
            
            # 验证预测显示数据
            self.assertIsInstance(display_predictions, list)
            self.assertEqual(len(display_predictions), 3)  # 3行测试数据
            
            # 验证每个预测项的结构
            for pred in display_predictions:
                self.assertIn('row_index', pred)
                self.assertIn('prediction', pred)
                self.assertIn('probability', pred)
                self.assertIn('risk_score', pred)
                self.assertIn('alert_triggered', pred)
                
            # 验证摘要信息
            self.assertIsInstance(summary, dict)
            self.assertIn('total_rows', summary)
            self.assertIn('benign', summary)
            self.assertIn('ddos', summary)
            self.assertIn('alerts', summary)
            self.assertIn('ddos_percentage', summary)
            self.assertIn('top_attackers_string', summary)
            
            self.assertEqual(summary['total_rows'], 3)
            self.assertEqual(summary['benign'] + summary['ddos'], 3)
            
            # 验证报告文件名
            self.assertIsInstance(full_report_filename, str)
            self.assertTrue(full_report_filename.startswith('report_'))
            
            # 验证警报数据
            self.assertIsInstance(display_alerts, list)
            
            # 验证报告文件是否生成
            full_report_path = os.path.join(self.reports_dir, full_report_filename)
            self.assertTrue(os.path.exists(full_report_path))
            
        except Exception as e:
            self.fail(f"处理上传文件时发生异常: {e}")

if __name__ == '__main__':
    unittest.main()