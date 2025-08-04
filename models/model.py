import torch
from torch import nn


class DDoSDetector(nn.Module):
    def __init__(self, input_dim):
        super(DDoSDetector, self).__init__()


        self.lstm1 = nn.LSTM(
            input_size=input_dim,
            hidden_size=10,
            bidirectional=True,
            batch_first=True
        )
        self.drop1 = nn.Dropout(0.2)


        self.lstm2 = nn.LSTM(
            input_size=20,  # 双向输出
            hidden_size=10,
            batch_first=True
        )
        self.drop2 = nn.Dropout(0.2)


        self.lstm3 = nn.LSTM(
            input_size=10,
            hidden_size=10,
            batch_first=True
        )
        self.drop3 = nn.Dropout(0.2)

        self.lstm4 = nn.LSTM(
            input_size=10,
            hidden_size=10,
            batch_first=True
        )
        self.drop4 = nn.Dropout(0.2)

        # 输出层
        self.fc = nn.Linear(10, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):

        x, _ = self.lstm1(x)
        x = self.drop1(x)


        x, _ = self.lstm2(x)
        x = self.drop2(x)

        x, _ = self.lstm3(x)
        x = self.drop3(x)


        x, (hn, cn) = self.lstm4(x)
        x = self.drop4(hn[-1])  # 取最后一层最后一个时间步的输出

        x = self.fc(x)
        return self.sigmoid(x)