from setuptools import setup, find_packages

setup(
    name="sip",
    version="0.0.3",
    author="Dr. Brandon Wiley",
    author_email="brandon@blanu.net",
    description="sip is a serial client for the iota system, written in python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/blanu/sip",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyserial>=3.5",
        "testify>=0.11.3",
        "iota-python>=0.0.15",
    ],
)
