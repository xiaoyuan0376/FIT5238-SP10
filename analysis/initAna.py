import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import warnings

warnings.filterwarnings('ignore')


# 数据加载与预处理
def load_and_preprocess_data(filepath):
    # 加载CSV数据
    features = pd.read_csv(filepath, delimiter=',', skiprows=0, low_memory=False)

    # 标签转换: BENIGN->0, DDoS->1
    features[' Label'].replace(['BENIGN', 'DDoS'], [0, 1], inplace=True)
    columns_to_drop = ['Flow ID'	, ' Source IP'	, ' Source Port',	 ' Destination IP'	, ' Destination Port',' Timestamp']
    for col in columns_to_drop:
        features.drop(columns=[col], inplace=True)

    # 处理异常值：无穷大和NaN
    features = features.replace([np.inf, -np.inf], np.nan)
    features = features.dropna()

    # 重命名标签列为'result'
    features.rename(columns={' Label': 'result'}, inplace=True)

    # 检查缺失值
    if features.isnull().sum().any():
        features = features.dropna()

    return features


#  特征工程与建模
def feature_analysis(data):
    # 分离特征和目标
    X = data.drop(columns='result')
    y = data['result']

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 特征标准化
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X.columns)

    # 训练随机森林
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # 特征重要性分析
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    return feature_importance, model


#  可视化与输出
def visualize_and_save(feature_importance, top_n=10):
    # 可视化TOP特征
    plt.figure(figsize=(14, 10))
    sns.barplot(
        x='Importance',
        y='Feature',
        data=feature_importance.head(top_n),
        palette='viridis'
    )
    plt.title(f'Top {top_n} Features Influencing DDoS Detection')
    plt.xlabel('Relative Importance Score')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)

    # 输出重要特征
    top_features = feature_importance.head(top_n)
    print(f"\n最有影响力的前{top_n}个变量:")
    print(top_features[['Feature', 'Importance']].reset_index(drop=True))

    # 保存结果
    feature_importance.to_csv('feature_importance_results.csv', index=False)
    top_features.to_csv('top_10_features.csv', index=False)


if __name__ == "__main__":
    filepath = "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"

    data = load_and_preprocess_data(filepath)
    feature_importance, _ = feature_analysis(data)
    visualize_and_save(feature_importance)

    print("分析完成！结果已保存到feature_importance.png和CSV文件")