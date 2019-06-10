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

        while True:
            new_clusters = [self._min_k(x) for x in X]

            if new_clusters == old_clusters:
                print("Training finished after {n_iters} iterations!".format(n_iters=n_iters))
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

        _centers_iter = self._centers_list[0]
        fig, ax = plt.subplots()

        # X 散点图
        self._scatter = ax.scatter(self.X[:, 0],
                                   self.X[:, 1],
                                   s=30,
                                   c="black",
                                   marker="o",
                                   label="slmethod kmeans")
        # 起始 中心
        ax.scatter(_centers_iter[:, 0], _centers_iter[:, 1], s=50, marker="^")
        # 结束 中心
        ax.scatter(self._centers[:, 0],
                   self._centers[:, 1],
                   s=300,
                   marker="*",
                   color='red')

        self._lines = []

        # X 与中心的连线
        for i in range(len(self.X)):
            x = self.X[i]
            x_i = self.predict(x)[0]
            points = np.vstack((x, _centers_iter[x_i]))
            line_i = ax.plot(points[:, 0],
                             points[:, 1],
                             color=self._colors[x_i],
                             linewidth=0.8,
                             alpha=0.5)
            self._lines.append(line_i)

        def update(iter):
            _centers_iter = self._centers_list[iter]
            title = "{} iter: {}".format(self.name, iter)
            plt.title(title)

            colors = []
            for i in range(len(self.X)):
                x = self.X[i]
                x_i = self.predict(x)[0]
                points = np.vstack((x, _centers_iter[x_i]))
                line_i = self._lines[i][0]
                line_i.set_xdata(points[:, 0])
                line_i.set_ydata(points[:, 1])
                colors.append(self._colors[x_i])

            self._scatter.set_color(colors)

            return self._lines, ax

        anim = FuncAnimation(fig,
                             update,
                             frames=len(self._centers_list),
                             interval=300)

        if name:
            anim.save(name, writer="imagemagick")
        else:
            plt.show()
