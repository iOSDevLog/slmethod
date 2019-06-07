"""
Statistical Learning Method 统计学习方法
==================================
《统计学习方法》的 Python 代码实现。
"""
import sys

name = "slmethod"

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release
#
# Dev branch marker is: "X.Y.dev" or "X.Y.devN" where N is an integer.
# "X.Y.dev0" is the canonical version of "X.Y.dev"
#
__version__ = "0.1.4"

try:
    # 此变量是由生成过程在 _builtins_ 中注入的。它用于在未生成二进制文件时启用 slmethod 子包的导入
    __SKLEARN_SETUP__
except NameError:
    __SKLEARN_SETUP__ = False

if __SKLEARN_SETUP__:
    sys.stderr.write("在生成过程中部分导入 slmethod\n")
else:
    from .utils._show_versions import show_versions

    __all__ = ["perceptron"]
