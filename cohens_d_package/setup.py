"""Setup script for cohens_d package."""

from setuptools import setup, find_packages
import os

# Read the README file for the long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A Python package for calculating Cohen's d effect size."

# Read version from __version__.py
def read_version():
    version_path = os.path.join(os.path.dirname(__file__), 'cohens_d', '__version__.py')
    version_dict = {}
    with open(version_path, 'r', encoding='utf-8') as f:
        exec(f.read(), version_dict)
    return version_dict['__version__']

setup(
    name="cohens-d-effect-size",
    version=read_version(),
    author="Dawit L. Gulta",
    author_email="dawit.lambebo@gmail.com",
    description="A Python package for calculating Cohen's d effect size",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DawitLam/cohens-d-scipy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Education",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/DawitLam/cohens-d-scipy/issues",
        "Source": "https://github.com/DawitLam/cohens-d-scipy",
        "Documentation": "https://github.com/DawitLam/cohens-d-scipy#readme",
    },
    keywords="cohen's d, effect size, statistics, research, psychology, data science",
    include_package_data=True,
    zip_safe=False,
)