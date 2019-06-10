import random
from sklearn.datasets import make_blobs
from slmethod.kmeans import KMeans
from sklearn.preprocessing import StandardScaler

random.seed(59)

X, y = make_blobs(n_samples=300,
                  n_features=2,
                  centers=3,
                  cluster_std=3,
                  random_state=42)
X = StandardScaler().fit_transform(X)
print(f"Shape of dataset: {X.shape}")

kmeans = KMeans(k=3)
kmeans.y = kmeans.fit(X)
print(f"kmeans._centers: {kmeans._centers}")
print(f"kmeans._centers_list: {kmeans._centers_list}")

kmeans.show_2d()
kmeans.show_anim("kmeans.gif")
