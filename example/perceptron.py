import numpy as np
from sklearn.datasets import make_blobs
from slmethod.perceptron import Perceptron
from sklearn.preprocessing import StandardScaler

X, y = make_blobs(n_samples=500,
                  n_features=2,
                  centers=2,
                  cluster_std=0.2,
                  random_state=59)

X = StandardScaler().fit_transform(X)
print(X)
print(f"Shape of dataset: {X.shape}")
y = np.where(y == 1, 1, -1)

# 原始感知机
origin_cls = Perceptron(dual=False)
origin_cls.fit(X, y)
origin_cls.show_anim()

# 对偶形式
dual_cls = Perceptron(dual=True)
dual_cls.fit(X, y)
dual_cls.show_2d()
