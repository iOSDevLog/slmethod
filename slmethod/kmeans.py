import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from slmethod.base import BaseEstimator
from matplotlib.collections import PathCollection


class KMeans(BaseEstimator):
    """
    # 聚类个数
    k = 2
    # 中心位置
    _centers = []
    # 每一轮迭带的中心位置
    _centers_list = []
    """

    def __init__(self, k=2):
        self.name = "KMeans"
        self.k = k

    def fit(self, X):
        self._setup_input(X)
        n_samples, _ = X.shape
        # 从 X 中随机获取 k 个元素做中心
        self._centers = np.array(
            random.sample(list(np.unique(X, axis=0)), self.k))

        old_clusters = None
        n_iters = 0
        self._centers_list = []

        while True:
            new_clusters = [self._min_k(x) for x in X]

            if new_clusters == old_clusters:
                print("Training finished after {n_iters} iterations!".format(
                    n_iters=n_iters))
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
    def _min_k(self, x, centers=None):
        if centers is None:
            centers = self._centers
        # 欧式距离
        dists = np.sqrt(np.sum((centers - x)**2, axis=1))
        return np.argmin(dists)

    def _predict(self, X, centers=None):
        X = np.atleast_2d(X)
        new_clusters = [self._min_k(x, centers) for x in X]
        return np.array(new_clusters)

    def show_anim(self, name=None):
        if (self.X.shape[1] != 2):
            raise ValueError("X must have 2d array.")

        _centers_iter = self._centers_list[0]
        fig, ax = plt.subplots()

        # X 散点图
        self._scatter = ax.scatter(self.X[:, 0],
                                   self.X[:, 1],
                                   s=10,
                                   c="black",
                                   marker="o",
                                   label="slmethod kmeans",
                                   alpha=0.5)

        self._lines = []

        # X 与中心的连线
        for i in range(len(self.X)):
            x = self.X[i]
            x_i = self.predict(x)[0]
            points = np.vstack((x, _centers_iter[x_i]))
            line_i = ax.plot(points[:, 0],
                             points[:, 1],
                             color=self._colors[x_i],
                             linewidth=0.3,
                             alpha=0.5)
            self._lines.append(line_i)

        _next_centers_iter = self._centers_list[1]
        # 下一个 中心
        self._next_iter_centers = ax.scatter(_next_centers_iter[:, 0],
                                             _next_centers_iter[:, 1],
                                             s=100,
                                             color=self._colors[:self.k])

        def update(iter):
            _centers_iter = self._centers_list[iter]
            title = "{} iter: {}".format(self.name, iter)
            plt.title(title)

            colors = []
            for i in range(len(self.X)):
                x = self.X[i]
                x_i = self._predict(x, _centers_iter)[0]
                points = np.vstack((x, _centers_iter[x_i]))
                line_i = self._lines[i][0]
                line_i.set_xdata(points[:, 0])
                line_i.set_ydata(points[:, 1])
                line_i.set_color(self._colors[x_i])
                colors.append(self._colors[x_i])

            self._scatter.set_color(colors)

            _next_centers_iter = self._centers_list[(iter + 1) %
                                                    len(self._centers_list)]
            self._next_iter_centers.set_offsets(_next_centers_iter)

            return self._lines, ax

        anim = FuncAnimation(fig,
                             update,
                             frames=len(self._centers_list),
                             interval=500)

        if name:
            anim.save(name, writer="imagemagick")
        plt.show()
