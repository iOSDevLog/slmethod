import pytest
import random
import numpy as np
from slmethod.kmeans import KMeans

random.seed(59)


@pytest.mark.parametrize("k", [1, 2])
def test_kmeans(k):
    X = np.array([
        [1.0, 1],
        [2, 2],
        [0, 0],
        [10, 10],
        [9, 11],
        [11, 9],
    ])
    kmeans = KMeans(k=k)
    kmeans.fit(X)

    test_X = [0.1, 0.1]

    cluster_x0 = kmeans.predict(X[0, :])
    predict_test_x = kmeans.predict(test_X)
    print(cluster_x0)
    print(predict_test_x)
    assert cluster_x0 == predict_test_x
