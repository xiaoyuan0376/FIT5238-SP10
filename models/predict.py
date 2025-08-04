import pandas as pd
import torch
from model import DDoSDetector
def csv_get_line(csv_name,x):
    # 指定需要提取的列名列表
    selected_columns = [
        " Fwd Packet Length Mean", " Fwd Packet Length Max", " Avg Fwd Segment Size",
        "Init_Win_bytes_forward", " Subflow Fwd Bytes", "Total Length of Fwd Packets",
        " act_data_pkt_fwd", " Bwd Packet Length Min", "Subflow Fwd Packets",
        " Fwd IAT Std"
    ]
    # 读取CSV并提取数据
    try:
        # 先读取列名以获取最后一列
        all_columns = pd.read_csv(csv_name, nrows=0).columns.tolist()
        last_column = all_columns[-1]

        # 只加载必要列 + 最后一列（避免内存浪费）
        df = pd.read_csv(csv_name, usecols=selected_columns + [last_column])

        # 提取第x行数据（若x超出范围则报错）
        row_data = df.iloc[x]
        print(row_data)
        return row_data.tolist()
    except IndexError:
        print(f"错误：文件总行数为{len(df)}，无法提取第{x}行")
    except FileNotFoundError:
        print("错误：文件不存在")



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = DDoSDetector(input_dim=10).to(device)
model.load_state_dict(torch.load('ddos_detection_model.pth', map_location=device))
model.eval()

# 3. 准备输入数据（单个样本）
# 选择1 从csv导入，参数为第n行
input_data = csv_get_line('../data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv',2333)
y = input_data[-1]
input_data = [input_data[:-1]]
print("label为(BENIGN:0,DDoS:1): "+y)
# 选择2 直接载入
# input_data = [[6.0000e+00, 6.0000e+00, 6.0000e+00, 2.2900e+02, 6.0000e+00, 6.0000e+00,
#          0.0000e+00, 6.0000e+00, 1.0000e+00, 0.0000e+00]]

# 修改预测时的数据重塑
input_tensor = torch.tensor(input_data, dtype=torch.float32).reshape(1, 1, -1)  # 变为 [1,1,10]

input_tensor = input_tensor.to(device)
# 4. 预测
with torch.no_grad():
    output = model(input_tensor)

    # 多分类任务：直接取argmax
    # predicted_class = torch.argmax(output).item()
    if(output>0.5):
        predicted_class ="DDoS"
    elif(0<output and output<0.5):
        predicted_class = "BENIGN"
    else:
        predicted_class = "ERROR"
    print(f"预测概率: {output.item():.4f}, 类别: {predicted_class}",end=' ')
