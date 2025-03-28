import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 加载数据
data = pd.read_csv('Advertising.csv', index_col=0)

# 打印数据信息
print("Data Preview:")
print(data.head(10))
print("\nDataset Shape:", data.shape)

# 数据集划分
X = data[['TV','Radio','Newspaper']]
# X = data[['TV','Radio']]   # 尝试删除Newspaper这个特征
y = data['Sales']
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=0)

# 各个广告的效果
plt.figure(figsize=(12, 8))

# TV广告效果
plt.subplot(311)
plt.scatter(data['TV'], y, c='b', marker='s', alpha=0.6)
plt.title('TV Advertising vs Sales')
plt.xlabel('TV Advertising Cost')
plt.ylabel('Sales')
plt.grid(True)

# Radio广告效果
plt.subplot(312)
plt.scatter(data['Radio'], y, c='g', marker='^', alpha=0.6)
plt.title('Radio Advertising vs Sales')
plt.xlabel('Radio Advertising Cost')
plt.ylabel('Sales')
plt.grid(True)

# Newspaper广告效果
plt.subplot(313)
plt.scatter(data['Newspaper'], y, c='r', marker='o', alpha=0.6)
plt.title('Newspaper Advertising vs Sales')
plt.xlabel('Newspaper Advertising Cost')
plt.ylabel('Sales')
plt.grid(True)

plt.tight_layout()
plt.show()

# 线性模型
model = LinearRegression(n_jobs=-1)

# 模型训练
model.fit(X_train, y_train)

# 预测与评估
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f'MSE: {mse:.2f}, R2: {r2:.2f}')
print(f"RMSE: {rmse:.2f}")
print(f'截距:{model.intercept_:.2f}')
print('系数:')
for feature, coefficient in zip(X.columns, model.coef_):
    print(f'{feature}: {coefficient:.2f}')

# 散点图：预测值 vs 真实值
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, c='steelblue', edgecolors='k', alpha=0.7)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
plt.title('Predicted vs Actual Sales')
plt.xlabel('Actual Sales')
plt.ylabel('Predicted Sales')
plt.grid(True)
plt.show()