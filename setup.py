
from setuptools import setup, find_packages

setup(
    name="lmdmap",
    version="1.0.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A tool for generating overviews of cropped microscopy tissue crosscuts for LMD.",
    packages=find_packages(),
    py_modules=["lmdmap"],
    install_requires=[
        "numpy",
        "pandas",
        "Pillow",
        "matplotlib",
        "pyairtable"
    ],
    entry_points={
        "console_scripts": [
            "lmdmap=lmdmap:main",
        ],
    },
    python_requires=">=3.6",
)
