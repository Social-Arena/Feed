"""Setup for Feed package"""

from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="twitter-feed-structure",
    version="1.0.0",
    author="Feed Module",
    description="Twitter/X data structures library",
    long_description=Path("README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/feed",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    install_requires=["pydantic>=2.0"],
    include_package_data=True,
    package_data={"feed": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
