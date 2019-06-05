import pytest
from slmethod.perceptron import Perceptron
import numpy as np


@pytest.mark.parametrize("dual, l_rate", [(True, None), (False, None),
                                          (False, 1), (False, 0.1),
                                          (False, 0.01)])
def test_perceptron(dual, l_rate):
    train_X = np.array([
        [-1, 3],
        [-5, 2],
        [-2, 5],
        [-6, 3],
        [-9, 7],
        [2, 6],
        [3, 3],
        [6, 6],
        [7, 2],
        [2, 3],
    ])
    train_y = np.array([
        -1,
        -1,
        -1,
        -1,
        -1,
        1,
        1,
        1,
        1,
        1,
    ])

    clf = Perceptron(dual=dual, l_rate=l_rate)
    clf.fit(train_X, train_y)
    test_X = np.array([[10, 3], [-29, 5]])
    test_y = np.array([1, -1])
    predict_y = clf.predict(test_X)
    assert np.array_equal(test_y, predict_y)
