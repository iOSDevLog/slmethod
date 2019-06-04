import numpy as np
from slmethod.base import BaseEstimator


class Perceptron(BaseEstimator):
    # 权重（权值）
    w = None
    # 偏置
    b = 0
    # 学习率
    l_rate = 0.1
    # 是否对偶
    dual = False

    def __init__(self, dual=0, l_rate=0.1):
        self.l_rate = l_rate
        self.dual = dual

    def sign(self, x, w, b):
        y = np.dot(x, w) + b
        return y

    def fit(self, X, y=None):
        self._setup_input(X, y)

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
                    self.w = self.w + self.l_rate * np.dot(
                        self.y[i], self.X[i])
                    self.b = self.b + self.l_rate * self.y[i]
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
                self.w = self.w + self.l_rate * np.dot(self.y[i], self.X[i])
                self.b = self.b + self.l_rate * self.y[i]
                i = 0
            else:
                i += 1

    def project(self, X):
        return np.dot(X, self.w) + self.b

    def _predict(self, X):
        X = np.atleast_2d(X)
        return np.sign(self.project(X))
