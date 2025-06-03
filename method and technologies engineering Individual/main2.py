import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Завантаження даних
file_path = "HotelCustomersDataset.xlsx"
data = pd.read_excel(file_path, nrows=5000)

# Попередній огляд даних
print("Інформація про дані:")
print(data.info())
print("\nПерші рядки:")
print(data.head())

# Заповнення пропущених значень
data['Age'] = data['Age'].fillna(data['Age'].mean())

# Видалення стовпців, які не використовуються
data = data.drop(['NameHash', 'DocIDHash'], axis=1)

# Перетворення категоріальних змінних у даммі-змінні
data = pd.get_dummies(data, columns=['Nationality', 'DistributionChannel', 'MarketSegment'], drop_first=True)

# Перевірка пропущених значень
print("\nПропущені значення:\n", data.isnull().sum())

# Заповнення пропущених значень для числових стовпців
for col in data.select_dtypes(include=np.number).columns:
    data[col] = data[col].fillna(data[col].mean())

# Нормалізація числових ознак
numerical_columns = data.select_dtypes(include=np.number).columns
scaler = StandardScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# Попередній огляд після обробки
print("\nОброблені дані (перші рядки):")
print(data.head(5))

# Використовуємо PCA для зменшення розмірності
pca = PCA(n_components=2)  # Зменшуємо до 2 компонент
reduced_data = pca.fit_transform(data[numerical_columns])

# Використання KMeans для кластеризації
kmeans = KMeans(n_clusters=3, random_state=42)
data['KMeans_Cluster'] = kmeans.fit_predict(reduced_data)

# Використання Agglomerative Clustering з альтернативним методом зв'язку
agglo = AgglomerativeClustering(n_clusters=3, linkage='ward')  # Замінили на 'average'
data['Agglo_Cluster'] = agglo.fit_predict(reduced_data)

# Використання DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
data['DBSCAN_Cluster'] = dbscan.fit_predict(reduced_data)

# Використання методу Spectral Clustering
from sklearn.cluster import SpectralClustering
spectral = SpectralClustering(n_clusters=3, affinity='nearest_neighbors', random_state=42)
data['Spectral_Cluster'] = spectral.fit_predict(reduced_data)

# Використання методу KMeans++
kmeans_plus_plus = KMeans(n_clusters=3, init='k-means++', random_state=42)
data['KMeansPlusPlus_Cluster'] = kmeans_plus_plus.fit_predict(reduced_data)

# Візуалізація PCA
plt.figure(figsize=(12, 8))

# Візуалізація результатів кластеризації для KMeans
plt.subplot(2, 3, 1)
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=data['KMeans_Cluster'], cmap='viridis', s=50)
plt.title("Кластери за допомогою KMeans")
plt.xlabel("Перша головна компонента")
plt.ylabel("Друга головна компонента")

# Візуалізація результатів кластеризації для Agglomerative Clustering
plt.subplot(2, 3, 2)
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=data['Agglo_Cluster'], cmap='viridis', s=50)
plt.title("Кластери за допомогою Agglomerative Clustering")
plt.xlabel("Перша головна компонента")
plt.ylabel("Друга головна компонента")

# Візуалізація результатів кластеризації для DBSCAN
plt.subplot(2, 3, 3)
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=data['DBSCAN_Cluster'], cmap='viridis', s=50)
plt.title("Кластери за допомогою DBSCAN")
plt.xlabel("Перша головна компонента")
plt.ylabel("Друга головна компонента")

# Візуалізація результатів кластеризації для Spectral Clustering
plt.subplot(2, 3, 4)
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=data['Spectral_Cluster'], cmap='viridis', s=50)
plt.title("Кластери за допомогою Spectral Clustering")
plt.xlabel("Перша головна компонента")
plt.ylabel("Друга головна компонента")

# Візуалізація результатів кластеризації для KMeans++
plt.subplot(2, 3, 5)
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=data['KMeansPlusPlus_Cluster'], cmap='viridis', s=50)
plt.title("Кластери за допомогою KMeans++")
plt.xlabel("Перша головна компонента")
plt.ylabel("Друга головна компонента")

# Показати графік
plt.tight_layout()
plt.show()

# Обчислення силуетного коефіцієнта для кожного методу
kmeans_silhouette = silhouette_score(reduced_data, data['KMeans_Cluster'])
agglo_silhouette = silhouette_score(reduced_data, data['Agglo_Cluster'])
dbscan_silhouette = silhouette_score(reduced_data, data['DBSCAN_Cluster'])
spectral_silhouette = silhouette_score(reduced_data, data['Spectral_Cluster'])
kmeans_plus_plus_silhouette = silhouette_score(reduced_data, data['KMeansPlusPlus_Cluster'])

print("\nSilhouette Score для KMeans:", kmeans_silhouette)
print("Silhouette Score для Agglomerative Clustering:", agglo_silhouette)
print("Silhouette Score для DBSCAN:", dbscan_silhouette)
print("Silhouette Score для Spectral Clustering:", spectral_silhouette)
print("Silhouette Score для KMeans++:", kmeans_plus_plus_silhouette)
