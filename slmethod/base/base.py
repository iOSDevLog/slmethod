import numpy as np
import matplotlib.pyplot as plt


class BaseEstimator:
    """
    # 样本特征集
    X = None
    # 样本标签集
    y = None
    # 类别个数
    k = 1
    # 估计器名称
    name = "Base"
    """

    # 绘图颜色
    _colors = (
        "red",
        "green",
        "blue",
        "magenta",
        "yellow",
        "cyan",
        "black",
        "white",
        "gray",
        "grey",
    )

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

        如果需要，通过从类似数组的对象转换，确保 X 和 y 存储为 numpy ndarrays

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
                self.k = len(np.unique(y))

            if y.size == 0:
                raise ValueError("Number of targets must be > 0")

        self.y = y

    def show_2d(self, name=None):
        if (self.X.shape[1] != 2):
            raise ValueError("X must have 2d array.")

        resolution = 0.01

        x1_min, x1_max = self.X[:, 0].min() - 1, self.X[:, 0].max() + 1
        x2_min, x2_max = self.X[:, 1].min() - 1, self.X[:, 1].max() + 1
        X1, X2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                             np.arange(x2_min, x2_max, resolution))
        y_ = self.predict(np.array([X1.ravel(), X2.ravel()]).T)
        y_ = y_.reshape(X1.shape)
        plt.contourf(X1, X2, y_, alpha=0.5)
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        y = self.predict(self.X)
        plt.scatter(self.X[:, 0], self.X[:, 1], c=y, s=10, marker="o")

        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.title(self.name)
        if name:
            plt.savefig(name)
        plt.show()
