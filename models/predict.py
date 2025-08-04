import torch

from models.model import DDoSDetector

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = DDoSDetector(input_dim=10).to(device)
model.load_state_dict(torch.load('ddos_detection_model.pth', map_location=device))
model.eval()

# 3. 准备输入数据（单个样本）
input_data = [[6.0000e+00, 6.0000e+00, 6.0000e+00, 2.5600e+02, 3.0000e+01, 3.0000e+01,
         4.0000e+00, 0.0000e+00, 5.0000e+00, 4.4810e+06]]
input_tensor = torch.tensor(input_data, dtype=torch.float32).unsqueeze(0)  # 添加batch维度[batch_size=1][5](@ref)
input_tensor = input_tensor.to(device)
# 4. 预测
with torch.no_grad():
    output = model(input_tensor)

    prediction_prob = torch.sigmoid(output).item()
    predicted_class = 1 if prediction_prob > 0.5 else 0
    # 多分类任务：直接取argmax
    # predicted_class = torch.argmax(output).item()

print(f"预测概率: {prediction_prob:.4f}, 类别: {predicted_class}")