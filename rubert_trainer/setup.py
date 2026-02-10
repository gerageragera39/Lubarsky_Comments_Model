"""
Setup configuration for ruBERT Fine-Tuning Studio
"""

from setuptools import setup, find_packages

with open("README_Model.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rubert-trainer",
    version="1.0.0",
    author="AI Developer",
    author_email="developer@example.com",
    description="Production GUI Application for fine-tuning ruBERT-large with hyperparameter tuning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "datasets>=2.0.0",
        "transformers>=4.20.0",
        "torch>=1.10.0",
        "PyQt6>=6.3.0",
    ],
    entry_points={
        "console_scripts": [
            "rubert-trainer=rubert_trainer.__main__:main",
        ],
    },
)