import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import warnings
import json

warnings.filterwarnings('ignore')


def load_and_preprocess_data_unlabeled(filepath):
    """
    加载不带标签的CSV数据
    """
    # 加载CSV数据
    features = pd.read_csv(filepath, delimiter=',', skiprows=0, low_memory=False)

    # 删除不需要的列
    columns_to_drop = ['Flow ID', ' Source IP', ' Source Port', ' Destination IP', ' Destination Port', ' Timestamp']
    for col in columns_to_drop:
        if col in features.columns:
            features.drop(columns=[col], inplace=True)

    # 处理异常值：无穷大和NaN
    features = features.replace([np.inf, -np.inf], np.nan)
    features = features.dropna()

    return features


def pca_analysis(data, n_components=10):
    """
    使用PCA进行特征重要性分析
    """
    # 特征标准化
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    
    # 执行PCA
    pca = PCA(n_components=min(n_components, len(data.columns)))
    pca.fit(scaled_data)
    
    # 计算特征重要性（基于PCA组件的贡献）
    # 重要性计算方法：每个特征在所有主成分中的贡献加权和
    feature_importance = pd.DataFrame({
        'Feature': data.columns,
        'Importance': np.sum(np.square(pca.components_.T) * pca.explained_variance_ratio_, axis=1)
    }).sort_values('Importance', ascending=False)
    
    return feature_importance, pca, scaler


def visualize_and_save_pca(feature_importance, top_n=10):
    """
    可视化并保存PCA分析结果
    """
    # 可视化TOP特征
    plt.figure(figsize=(14, 10))
    sns.barplot(
        x='Importance',
        y='Feature',
        data=feature_importance.head(top_n),
        palette='viridis'
    )
    plt.title(f'Top {top_n} Features Influencing Network Traffic (PCA Analysis)')
    plt.xlabel('Relative Importance Score')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)

    # 输出重要特征
    top_features = feature_importance.head(top_n)
    print(f"\n最有影响力的前{top_n}个变量 (基于PCA分析):")
    print(top_features[['Feature', 'Importance']].reset_index(drop=True))

    # 保存结果
    feature_importance.to_csv('feature_importance_results.csv', index=False)
    top_features.to_csv('top_10_features.csv', index=False)