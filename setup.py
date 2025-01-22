from setuptools import setup, find_packages

setup(
    name="lmdmap",
    version="1.0.0",
    author="Antton Alberdi",
    author_email="anttonalberdi@gmail.com",
    description="Crop cryosections and output an overview image and associated csv with the pixel coordinates of the microsamples.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["lmdmap"],
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "lmdmap=lmdmap:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
