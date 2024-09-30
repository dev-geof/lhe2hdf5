# LHE to HDF5 File Converter

## Introduction

The `lhe2hdf5` tool provides a streamlined solution for converting "Les Houches Event" (LHE) files into HDF5 format. The LHE file format is widely used in high-energy physics simulations to store particle event data, including the kinematic information of particles produced in collision events. Both uncompressed (.lhe) and compressed (.lhe.gz) LHE files can be read by the tool. The processed particle data, including particle ID, status, momentum components, energy, mass, transverse momentum, and rapidity, as well as the event weights are saved in an HDF5 file for efficient storage and retrieval.

## Getting the Code

To get started you can clone the `lhe2hdf5` repository from GitHub using the following command:
```bash
git clone https://github.com/dev-geof/lhe2hdf5.git
```

## Installation

To install `lhe2hdf5` and its dependencies you can use the following command:
```bash
python -m pip install -e . -r requirements.txt
```

## Usage

### Script Invocation

```bash
lhe2hdf5 -i lhe_dir/ -o output.hdf5
```

### Parameters

- **i** (str): Path to the directory containing LHE files.
- **o** (str): Path to the output HDF5 file.

## License

`lhe2hdf5` is distributed under the [MIT License](LICENSE), granting users the freedom to use, modify, and distribute the code. Contributions, bug reports, and suggestions for improvements are warmly welcomed.
