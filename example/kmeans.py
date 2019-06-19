from sklearn.datasets import make_blobs
from slmethod.kmeans import KMeans
from sklearn.preprocessing import StandardScaler

X, y = make_blobs(n_samples=1000,
                  n_features=2,
                  centers=3,
                  cluster_std=1,
                  random_state=0)
X = StandardScaler().fit_transform(X)
print(f"Shape of dataset: {X.shape}")

kmeans = KMeans(k=3)
kmeans.y = kmeans.fit(X)
print(f"kmeans._centers: {kmeans._centers}")
print(f"kmeans._centers_list: {kmeans._centers_list}")

kmeans.show_2d("kmeans.png")
kmeans.show_anim("kmeans.gif")
