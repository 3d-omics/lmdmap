from setuptools import setup, find_packages

setup(
    name="lmdmap",  # Replace with a unique name for your tool
    version="1.0.0",
    author="Antton Alberdi",
    author_email="anttonalberdi@gmail.com",
    description="Crop cryosections and output an overview image and associated csv with the pixel coordinates of the microsamples.",
    long_description=open("README.md").read(),  # Optional if README exists
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["lmdmap"],  # Your script as a module
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "lmdmap=lmdmap:main",  # Replace with your module and function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
