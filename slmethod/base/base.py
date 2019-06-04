import numpy as np


class BaseEstimator:
    X = None
    y = None

    def fit(self, X, y=None):
        self._setup_input(X, y)

    def predict(self, X=None):
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        if self.X is not None:
            return self._predict(X)
        else:
            raise ValueError("You must call `fit` before `predict`")

    def _predict(self, X=None):
        raise NotImplementedError()

    def _setup_input(self, X, y=None):
        """确保估计器的输入符合预期格式。

        如果需要，通过从类似数组的对象转换，确保 X 和 y 存储为 numpy ndarrays。 

        Parameters
        ----------
        X : array-like
        y : array-like
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        if X.size == 0:
            raise ValueError("Number of features must be > 0")

        if X.ndim == 1:
            self.n_samples, self.n_features = 1, X.shape
        else:
            self.n_samples, self.n_features = X.shape[0], np.prod(X.shape[1:])

        self.X = X

        if y is not None:
            if not isinstance(y, np.ndarray):
                y = np.array(y)

            if y.size == 0:
                raise ValueError("Number of targets must be > 0")

        self.y = y
