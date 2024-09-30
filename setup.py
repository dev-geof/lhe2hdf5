import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lhe2hdf5",
    version="0.0.1",
    author="Geoffrey Gilles",
    description="LHE to HDF5 file converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-geof/lhe2hdf5",
    packages=setuptools.find_packages(),
    install_requires=[
        "h5py>=3.10.0",
        "numpy>=1.24.4",
        "lxml>=5.3.0",
        "tqdm>=4.66.3",
    ],
    entry_points={
        "console_scripts": [
            "lhe2hdf5=src.lhe2hdf5:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.9.13",
)
