import numpy as np
import matplotlib.pyplot as plt
from slmethod.base import BaseEstimator
from matplotlib.animation import FuncAnimation
from functools import reduce


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
    # 对偶 alpha
    _alpha = 1
    # gram 矩阵，加速对偶
    _gram_matrix = None

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

    # 对偶形式
    def _fit_dual(self):
        """
        对偶形式中训练实例仅以内积的形式出现
        先求出 Gram 矩阵，能大大减少计算量
        """
        n_samples, n_features = self.X.shape
        self._alpha = np.zeros(n_samples, dtype=np.float64)
        self.w = np.zeros(n_features, dtype=np.float64)
        self.b = 0.0

        self._cal_gram_matrix()

        i = 0
        while i < n_samples:
            if self._dual_judge(i) <= 0:
                self._alpha[i] += self.l_rate
                self.b += self.l_rate * self.y[i]
                i = 0
            else:
                i += 1

        for i in range(n_samples):
            self.w += self._alpha[i] * self.X[i] * self.y[i]

    # 对偶判定条件
    def _dual_judge(self, i):
        sum_array = self._alpha * self.y * self._gram_matrix[:, i]
        return self.y[i] * reduce(lambda x, y: x+y, sum_array, self.b)

    # 计算Gram Matrix
    def _cal_gram_matrix(self):
        n_sample = self.X.shape[0]
        self._gram_matrix = np.zeros((n_sample, n_sample))

        for i in range(n_sample):
            for j in range(n_sample):
                self._gram_matrix[i][j] = np.sum(self.X[i] * self.X[j])

    def project(self, X):
        return np.dot(X, self.w) + self.b

    def _predict(self, X):
        X = np.atleast_2d(X)
        return np.sign(self.project(X))

    def show_anim(self, name=None):
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
            (index, w, b) = self._wbs[-1]
            y_points = -(w[0] * x_points + b) / w[1]
            line.set_ydata(y_points)
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
