#! /usr/bin/env python3

import setuptools
import builtins
from os import path

# 导入一个不需要编译代码的受限版本的 slmethod
import slmethod

# 可以检测到它是否被安装程序加载, 以避免尝试加载尚未生成的组件
builtins.__SKLEARN_SETUP__ = True

here = path.abspath(path.dirname(__file__))

# 安装依赖
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = \
    [x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")]

SCIPY_MIN_VERSION = "1.3"
NUMPY_MIN_VERSION = "1.16"
JOBLIB_MIN_VERSION = "0.13"

DISTNAME = "slmethod"
VERSION = slmethod.__version__
DESCRIPTION = "Statistical Learning Method package"
with open("README.md") as f:
    LONG_DESCRIPTION = f.read()
URL = "https://github.com/iOSDevLog/slmethod"
AUTHOR = "Xianhua Jia"
AUTHOR_EMAIL = "iosdevlog@iosdevlog.com"
DOWNLOAD_URL = "https://pypi.org/project/slmethod/#files"
LICENSE = "MIT"
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/iOSDevLog/slmethod/issues",
    "Documentation": "https://github.com/iOSDevLog/slmethod",
    "Source Code": "https://github.com/iOSDevLog/slmethod"
}

setuptools.setup(
    name=DISTNAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    license=LICENSE,
    packages=setuptools.find_packages(exclude=["contrib", "docs", "tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    install_requires=install_requires,
    dependency_links=dependency_links,
    setup_requires=[
        "numpy>={}".format(NUMPY_MIN_VERSION),
        "scipy>={}".format(SCIPY_MIN_VERSION),
        "joblib>={}".format(JOBLIB_MIN_VERSION)
    ],
)
