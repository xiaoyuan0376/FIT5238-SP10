import sys
import os
import unittest
import pandas as pd
import time
import tempfile

# Add the project root directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.prediction import run_prediction
from analysis_handler import process_uploaded_file

class TestPerformance(unittest.TestCase):
    """性能测试 - 对应文档中的FT-004, FT-005"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.reports_dir = os.path.join(self.temp_dir, 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # 定义必需的特征列
        self.required_columns = [
            " Fwd Packet Length Mean", " Fwd Packet Length Max", " Avg Fwd Segment Size",
            "Init_Win_bytes_forward", " Subflow Fwd Bytes", "Total Length of Fwd Packets",
            " act_data_pkt_fwd", " Bwd Packet Length Min", "Subflow Fwd Packets",
            " Fwd IAT Std"
        ]
        
    def create_large_dataset(self, num_rows: int) -> pd.DataFrame:
        """创建大型测试数据集"""
        import numpy as np
        
        data = {}
        for col in self.required_columns:
            # 生成随机数据
            data[col] = np.random.uniform(0, 1000, num_rows)
            
        return pd.DataFrame(data)
    
    # FT-004 批处理性能测试将通过手动上传大CSV文件进行测试
    
    def test_model_inference_speed(self):
        """测试模型推理速度 - 对应文档中的FT-005"""
        # 创建小型测试数据用于单次预测测试
        single_prediction_data = self.create_large_dataset(1)
        
        # 测试单次预测时间
        num_iterations = 10
        total_time = 0
        
        for i in range(num_iterations):
            start_time = time.time()
            
            predictions, probabilities = run_prediction(single_prediction_data)
            
            end_time = time.time()
            iteration_time = end_time - start_time
            total_time += iteration_time
            
            # 验证返回结果
            self.assertEqual(len(predictions), 1)
            self.assertEqual(len(probabilities), 1)
            
        average_time = total_time / num_iterations
        print(f"\nAverage single prediction time: {average_time:.4f} seconds")
        print(f"Average single prediction time: {average_time*1000:.2f} milliseconds")
        
        # 验证单次预测时间小于1秒
        self.assertLess(average_time, 1.0, 
            f"Average single prediction time {average_time:.4f} seconds exceeds 1 second requirement")
        
        # 测试批量预测性能
        batch_sizes = [10, 50, 100]
        
        for batch_size in batch_sizes:
            with self.subTest(batch_size=batch_size):
                batch_data = self.create_large_dataset(batch_size)
                
                start_time = time.time()
                predictions, probabilities = run_prediction(batch_data)
                end_time = time.time()
                
                batch_time = end_time - start_time
                time_per_prediction = batch_time / batch_size
                
                print(f"Batch prediction for {batch_size} records took: {batch_time:.4f} seconds")
                print(f"Average time per record: {time_per_prediction:.4f} seconds")
                
                # 验证返回结果
                self.assertEqual(len(predictions), batch_size)
                self.assertEqual(len(probabilities), batch_size)
                
                # 验证批量处理效率（每条记录应该比单次预测更快）
                self.assertLess(time_per_prediction, average_time * 1.5, 
                    f"Batch processing efficiency below expectation, {time_per_prediction:.4f} seconds per record")
    
    def test_memory_usage(self):
        """测试内存使用情况"""
        import psutil
        import gc
        
        # 记录开始时的内存使用
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 处理较大数据集
        large_data = self.create_large_dataset(5000)
        
        # 执行预测
        predictions, probabilities = run_prediction(large_data)
        
        # 记录处理后的内存使用
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory
        
        print(f"\nInitial memory usage: {initial_memory:.2f} MB")
        print(f"Peak memory usage: {peak_memory:.2f} MB")
        print(f"Memory increase: {memory_increase:.2f} MB")
        print(f"Memory increase per 1000 records: {(memory_increase/5000)*1000:.2f} MB")
        
        # 清理内存
        del large_data, predictions, probabilities
        gc.collect()
        
        # 验证内存增长在合理范围内 (例如不超过500MB)
        self.assertLess(memory_increase, 500, 
            f"Memory increase {memory_increase:.2f} MB exceeds expected 500MB")
    
    def test_concurrent_processing(self):
        """测试并发处理能力"""
        import threading
        import queue
        
        # 创建多个小数据集
        num_threads = 3
        dataset_size = 100
        results_queue = queue.Queue()
        
        def process_data(thread_id):
            try:
                data = self.create_large_dataset(dataset_size)
                start_time = time.time()
                predictions, probabilities = run_prediction(data)
                end_time = time.time()
                
                processing_time = end_time - start_time
                results_queue.put({
                    'thread_id': thread_id,
                    'processing_time': processing_time,
                    'success': True,
                    'predictions_count': len(predictions)
                })
            except Exception as e:
                results_queue.put({
                    'thread_id': thread_id,
                    'success': False,
                    'error': str(e)
                })
        
        # 启动多个线程
        threads = []
        overall_start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=process_data, args=(i,))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        overall_end_time = time.time()
        overall_time = overall_end_time - overall_start_time
        
        # 收集结果
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        
        print(f"\nConcurrent processing test results:")
        print(f"Overall processing time: {overall_time:.2f} seconds")
        print(f"Number of threads: {num_threads}")
        
        successful_results = [r for r in results if r['success']]
        
        # 验证所有线程都成功完成
        self.assertEqual(len(successful_results), num_threads, 
            f"Only {len(successful_results)}/{num_threads} threads completed successfully")
        
        # 验证每个线程的结果
        for result in successful_results:
            print(f"Thread {result['thread_id']}: {result['processing_time']:.2f} seconds, {result['predictions_count']} predictions")
            self.assertEqual(result['predictions_count'], dataset_size)

if __name__ == '__main__':
    unittest.main()