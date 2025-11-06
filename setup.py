"""
Setup configuration for the Feed package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="twitter-feed-simulator",
    version="1.0.0",
    author="Feed Module",
    author_email="",
    description="A comprehensive Twitter simulation and data modeling package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/feed",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="twitter, simulation, social-media, data-modeling, api",
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "feed-simulate=examples.simulation_demo:main",
        ],
    },
    include_package_data=True,
    package_data={
        "feed": ["py.typed"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/feed/issues",
        "Source": "https://github.com/yourusername/feed",
        "Documentation": "https://github.com/yourusername/feed/blob/main/README.md",
    },
    zip_safe=False,
)
