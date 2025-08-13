import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from model import DDoSDetector

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 数据预处理
veri = pd.read_csv("Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv", delimiter=',', skiprows=0, low_memory=False)
veri[' Label'].replace(['BENIGN', 'DDoS'], [0, 1], inplace=True)
moddf = veri.dropna()
features = [" Fwd Packet Length Mean", " Fwd Packet Length Max", " Avg Fwd Segment Size",
            "Init_Win_bytes_forward", " Subflow Fwd Bytes", "Total Length of Fwd Packets",
            " act_data_pkt_fwd", " Bwd Packet Length Min", "Subflow Fwd Packets",
            " Fwd IAT Std", " Label"]
X = moddf[features].copy()
print(X.loc[:10].to_numpy())
giris = X.iloc[:, 0:10]
cikis = X.iloc[:, -1]

# 分割数据集
xtrain, xtest, ytrain, ytest = train_test_split(giris, cikis, test_size=0.05)
x_train, y_train = np.array(xtrain), np.array(ytrain)
x_test, y_test = np.array(xtest), np.array(ytest)
print(x_test[:5])
# 重塑为3D张量 (样本数, 序列长度=1, 特征数=10)
x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

# 转换为PyTorch张量
x_train_tensor = torch.tensor(x_train, dtype=torch.float32).to(device)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1).to(device)
x_test_tensor = torch.tensor(x_test, dtype=torch.float32).to(device)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1).to(device)

# 数据加载器
train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)



# 初始化模型 (注意输入维度为11个特征)
model = DDoSDetector(input_dim=x_train.shape[-1]).to(device)

# 损失函数和优化器
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters())


# 训练函数
def train_model(model, train_loader, epochs=10):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # 计算准确率
            predicted = (outputs > 0.5).float()
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
            total_loss += loss.item()

        accuracy = 100 * correct / total
        avg_loss = total_loss / len(train_loader)
        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.4f}, Acc: {accuracy:.2f}%')

    return model


# 评估函数
def evaluate_model(model, x_test, y_test):
    model.eval()
    with torch.no_grad():
        print(x_test.size())
        outputs = model(x_test)
        print("xtest", "y_test", "output")
        # 重塑维度以正确连接
        x_test_reshaped = x_test.view(x_test.size(0), -1)  # 将3D重塑为2D
        # 连接重塑后的x_test和outputs
        combined = torch.cat([x_test_reshaped,y_test ,outputs], dim=1)
        print("xtest_outputs_y_test样本:")
        print(combined[:5])  # 仅打印前5个样本示例

        loss = criterion(outputs, y_test)
        predicted = (outputs > 0.5).float()
        accuracy = (predicted == y_test).float().mean()

    print(f'Test Loss: {loss.item():.4f}, Test Acc: {accuracy.item() * 100:.2f}%')
    return predicted.cpu().numpy()


# 训练和评估
model = train_model(model, train_loader, epochs=20)
test_predictions = evaluate_model(model, x_test_tensor, y_test_tensor)

# 保存模型
torch.save(model.state_dict(), 'ddos_detection_model_20.pth')
print("Model saved successfully.")