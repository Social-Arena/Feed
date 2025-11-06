"""
Setup configuration for the Feed package - Twitter Data Structure Library
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="twitter-feed-structure",
    version="1.0.0",
    author="Feed Module",
    author_email="",
    description="A clean Python package for Twitter/X data structures - build your simulator on top!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/feed",
    packages=find_packages(exclude=["tests", "docs"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    keywords="twitter, data-structure, social-media, twitter-api, dataclass",
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
