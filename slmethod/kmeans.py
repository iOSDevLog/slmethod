import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from slmethod.base import BaseEstimator


class KMeans(BaseEstimator):
    # 聚类个数
    k = 2
    # 中心位置
    _centers = []
    # 每一轮迭带的中心位置
    _centers_list = []

    def __init__(self, k=2):
        self.k = k

    def fit(self, X):
        self._setup_input(X)
        n_samples, _ = X.shape
        # 从 X 中随机获取 k 个元素做中心
        self._centers = np.array(
            random.sample(list(np.unique(X, axis=0)), self.k))

        old_clusters = None
        n_iters = 0

        while True:
            new_clusters = [self._min_k(x) for x in X]

            if new_clusters == old_clusters:
                print(f"Training finished after {n_iters} iterations!")
                return

            old_clusters = new_clusters
            n_iters += 1

            for cluster_i in range(self.k):
                # 计算新的中心
                points_idx = np.where(np.array(new_clusters) == cluster_i)
                xi = X[points_idx]
                self._centers[cluster_i] = xi.mean(axis=0)

            self._centers_list.append(np.copy(self._centers))

    # 找出点 x 离 k 个中心最近一个聚类
    def _min_k(self, x):
        # 欧式距离
        dists = np.sqrt(np.sum((self._centers - x)**2, axis=1))
        return np.argmin(dists)

    def _predict(self, X):
        X = np.atleast_2d(X)
        new_clusters = [self._min_k(x) for x in X]
        return np.array(new_clusters)

    def show_anim(self, name=None):
        if (self.X.shape[1] != 2):
            raise ValueError("X must have 2d array.")

        fig, ax = plt.subplots()

        scatter = ax.scatter(self.X[:, 0], self.X[:, 1], s=30, marker="o")

        def update(iter):
            _centers_iter = self._centers_list[iter]
            title = "iter: {}".format(iter)
            plt.title(title)
            # update center
            ax.scatter(_centers_iter[:, 0],
                       _centers_iter[:, 1],
                       s=50,
                       label=title,
                       marker="^")

            return scatter, ax

        anim = FuncAnimation(fig,
                             update,
                             frames=len(self._centers_list),
                             interval=200)

        if name:
            anim.save(name, writer="imagemagick")
        else:
            plt.show()
