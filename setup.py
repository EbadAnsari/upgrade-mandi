"""
Setup configuration for the Upgrade Mandi project.
This makes the project installable as a Python package.
"""

from setuptools import setup, find_packages

setup(
    name="upgrade_mandi",
    version="1.0.0",
    description="Data analysis project for Upgrade Mandi",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "numpy", 
        "jupyter",
        "matplotlib",
        "seaborn",
        "openpyxl",
        "xlrd"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
