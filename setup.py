import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slmethod",
    version="0.0.3",
    author="iOSDevLog",
    author_email="iosdevlog@iosdevlog.com",
    description="Statistical Learning Method package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iOSDevLog/slmethod",
    license='MIT',
    packages=setuptools.find_packages(),
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
)
