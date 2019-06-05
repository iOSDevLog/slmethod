import numpy as np
import matplotlib.pyplot as plt
from slmethod.base import BaseEstimator
from matplotlib.animation import FuncAnimation


class Perceptron(BaseEstimator):
    # 权重（权值）
    w = None
    # 偏置
    b = 0
    # 学习率
    l_rate = 0.1
    # 是否对偶
    dual = False
    # 内部绘图使用 (i, w, b)
    _wbs = []

    def __init__(self, dual=True, l_rate=None):
        if l_rate is not None:
            self.l_rate = l_rate
        self.dual = dual

    def sign(self, x, w, b):
        y = np.dot(x, w) + b
        return y

    def fit(self, X, y):
        self._setup_input(X, y)
        check_y = np.all(np.isin(y, [-1, 1]))
        if not check_y:
            raise ValueError("`y` must in {-1, 1}")

        self._wbs = []

        if self.dual:
            self._fit_dual()
        else:
            self._fit()

    # 原始
    def _fit(self):
        n_samples, n_features = self.X.shape
        self.w = np.zeros(n_features, dtype=np.float64)
        self.b = 0.0

        is_finished = False
        while not is_finished:
            count = 0  # 记录误分类点的数目
            for i in range(n_samples):
                if self.y[i] * self.sign(self.w, self.X[i], self.b) <= 0:
                    self.w += self.l_rate * np.dot(self.y[i], self.X[i])
                    self.b += self.l_rate * self.y[i]
                    self._wbs.append((i, self.w, self.b))
                    count += 1

                if count == 0:
                    is_finished = True

    # 对偶
    def _fit_dual(self):
        n_samples, n_features = self.X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0

        i = 0
        while i < n_samples:
            if self.y[i] * self.sign(self.w, self.X[i], self.b) <= 0:
                self.w += self.l_rate * np.dot(self.y[i], self.X[i])
                self.b += self.l_rate * self.y[i]
                self._wbs.append((i, self.w, self.b))
                i = 0
            else:
                i += 1

    def project(self, X):
        return np.dot(X, self.w) + self.b

    def _predict(self, X):
        X = np.atleast_2d(X)
        return np.sign(self.project(X))

    def show2d(self, name=None):
        if (self.X.shape[1] != 2):
            raise ValueError("X must have 2d array.")

        # 取最小值与最大值用于画直线
        minX = np.min(self.X[:, 0])
        maxX = np.max(self.X[:, 0])
        x_points = np.array([minX, maxX])

        fig, ax = plt.subplots()

        ax.scatter(self.X[:, 0], self.X[:, 1], c=self.y, s=1, marker="o")
        line, = ax.plot(x_points,
                        np.zeros(len(x_points)),
                        "r-",
                        linewidth=2,
                        label="slmethod perceptron")

        def init():
            line.set_ydata(np.zeros(len(x_points)))
            return line,

        def update(iter):
            (index, w, b) = self._wbs[iter]
            # title
            title = "iter: {}, index: {}".format(iter, index)
            plt.title(title)
            # show w and b
            wb = "w0: {}, w1: {}, b: {}".format(w[0], w[1], b)
            ax.set_xlabel(wb)
            # update y
            y_points = -(w[0] * x_points + b) / w[1]
            line.set_ydata(y_points)

            return line, ax

        ax.legend()
        anim = FuncAnimation(fig,
                             update,
                             init_func=init,
                             frames=len(self._wbs),
                             interval=200)

        if name:
            anim.save(name, writer="imagemagick")
        else:
            plt.show()
