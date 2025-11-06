"""
Setup configuration for the Feed module
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="feed",
    version="1.0.0",
    author="Feed Module",
    description="A comprehensive social media feed data structure and simulation module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/feed",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
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
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies required
        # Uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "enhanced": [
            "pydantic>=2.0.0",  # For advanced validation
            "python-dateutil>=2.8.0",  # For better date handling
            "pytz>=2023.3",  # For timezone support
            "faker>=18.0.0",  # For more realistic data generation
            "numpy>=1.20.0",  # For statistical simulations
        ],
    },
    entry_points={
        "console_scripts": [
            "feed-simulate=example_simulation:main",
        ],
    },
    include_package_data=True,
    package_data={
        "feed": ["*.md", "*.txt"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/feed/issues",
        "Source": "https://github.com/yourusername/feed",
        "Documentation": "https://github.com/yourusername/feed/blob/main/README.md",
    },
)
