#! /usr/bin/env python3

import setuptools
import builtins

# 可以检测到它是否被安装程序加载, 以避免尝试加载尚未生成的组件
builtins.__SKLEARN_SETUP__ = True

# 导入一个不需要编译代码的受限版本的 slmethod
import slmethod

SCIPY_MIN_VERSION = '1.3'
NUMPY_MIN_VERSION = '1.16'
JOBLIB_MIN_VERSION = '0.13'

DISTNAME = 'slmethod'
VERSION = slmethod.__version__
DESCRIPTION = 'Statistical Learning Method package'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()
URL = 'https://github.com/iOSDevLog/AIDevLog'
AUTHOR = 'Xianhua Jia'
AUTHOR_EMAIL = 'iosdevlog@iosdevlog.com'
DOWNLOAD_URL = 'https://pypi.org/project/slmethod/#files'
LICENSE = 'MIT'
PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/iOSDevLog/slmethod/issues',
    'Documentation': 'https://github.com/iOSDevLog/slmethod',
    'Source Code': 'https://github.com/iOSDevLog/slmethod'
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
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
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
    install_requires=[
        'numpy>={}'.format(NUMPY_MIN_VERSION),
        'scipy>={}'.format(SCIPY_MIN_VERSION),
        'joblib>={}'.format(JOBLIB_MIN_VERSION)
    ],
)
