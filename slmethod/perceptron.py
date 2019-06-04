import numpy as np
from slmethod.base import BaseEstimator


class Perceptron(BaseEstimator):
    # 权重
    w = None
    # 偏置
    b = 0
    # 学习率
    l_rate = 1
    # 是否对偶
    dual = 0

    def __init__(self, dual=0):
        self.dual = dual

    def fit(self, X, y=None):
        self._setup_input(X, y)

        if self.dual:
            self._fit_dual()
        else:
            self._fit()

    def _fit(self):
        n_samples, n_features = self.X.shape
        self.w = np.zeros(n_features, dtype=np.float64)
        self.b = 0.0

        for i in range(n_samples):
            if self.predict(self.X[i])[0] != self.y[i]:
                self.w += self.y[i] * self.X[i]
                self.b += self.y[i]

    def _fit_dual(self):
        n_samples, n_features = self.X.shape
        self.w = np.zeros(n_features, dtype=np.float64)
        self.b = 0.0

        i = 0
        while i < n_samples:
            if self.y[i] * (np.dot(self.w, self.X[i]) + self.b) <= 0:
                self.w = self.w + self.l_rate * np.dot(self.y[i], self.X[i])
                self.b = self.b + self.l_rate * self.y[i]
                i = 0
            else:
                i = i + 1

    def project(self, X):
        return np.dot(X, self.w) + self.b

    def _predict(self, X):
        X = np.atleast_2d(X)
        return np.sign(self.project(X))
