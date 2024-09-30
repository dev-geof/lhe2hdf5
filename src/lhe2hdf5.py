import os
import argparse
import numpy as np
import math
import h5py
import gzip
from lxml import etree
from tqdm import tqdm


def read_lhe_file(file_path):
    """
    Read an LHE file (possibly compressed) and extract particle information and event weights.

    Args:
        file_path (str): Path to the LHE file.

    Returns:
        tuple: Tuple containing particle information (pid, status, px, py, pz, E)
               and event weights.
    """

    if file_path.endswith(".gz"):
        with gzip.open(file_path, "rt") as f:  # Open the compressed file for reading
            lhe_data = f.read()  # Read the contents of the compressed file
    else:
        with open(file_path, "r") as f:
            lhe_data = f.read()

    tree = etree.parse(file_path)
    root = tree.getroot()

    data = []
    weights = []
    # Find all <event> tags representing collision events
    events = root.findall(".//event")
    for event in tqdm(events):
        metadata = event.text.strip().split("\n")[0]  # First line containing metadata
        # Extract event weight from the metadata
        weight = float(metadata.split()[2])  # Assuming the third value is the weight
        particles = event.text.strip().split("\n")[
            1:
        ]  # Skip first line containing metadata

        data_particles = []
        for particle in particles:
            values = particle.split()

            # Print out for debugging purpose
            # print("Number of values:", len(values))  # Print the number of values in each particle line
            # print("Values:", values)  # Print the values for debugging purposes

            # Extract particle information: ID, status, momentum components (px, py, pz), energy (E) and mass (m)
            pid, status, _, _, _, _, px, py, pz, E, m, _, _ = map(float, values)
            if status == 1:  # Final state particle
                pt = math.sqrt((px * px) + (py * py))
                y = 0.5 * math.log((E + pz) / (E - pz))
                data_particles.append((pid, status, px, py, pz, pt, E, m, y))

        data.append(data_particles)
        weights.append(weight)

    return np.array(
        data,
        dtype=[
            ("pid", float),
            ("status", float),
            ("px", float),
            ("py", float),
            ("pz", float),
            ("pt", float),
            ("E", float),
            ("m", float),
            ("y", float),
        ],
    ), np.array(weights)


def process_lhe_files(input_dir, output_file):
    """
    Process a directory containing LHE files (including subdirectories) and store particle information and event weights in a single HDF5 file.

    Args:
        input_dir (str): Path to the directory containing LHE files (including subdirectories).
        output_file (str): Path to the output HDF5 file.
    """
    combined_data = []
    combined_weights = []

    # Recursively search for LHE files in input_dir and its subdirectories
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith(".lhe") or file_name.endswith(".lhe.gz"):
                file_path = os.path.join(root, file_name)
                data, weights = read_lhe_file(file_path)
                combined_data.extend(data)
                combined_weights.extend(weights)

    combined_data = np.array(combined_data)
    combined_weights = np.array(combined_weights)

    # Write the combined data and weights to the HDF5 file
    with h5py.File(output_file, "w") as f:
        f.create_dataset("data", data=combined_data)
        f.create_dataset("weights", data=combined_weights)


def main():
    """
    Entry point for the LHE to HDF5 conversion script.

    Parses command-line arguments and invokes the process_lhe_files function.
    """
    parser = argparse.ArgumentParser(description="LHE to HDF5 file converter")

    parser.add_argument(
        "-i",
        action="store",
        dest="input_dir",
        default="LHE_dir",
        help="Path to the directory containing LHE files.",
    )

    parser.add_argument(
        "-o",
        action="store",
        dest="output_file",
        default="output.h5",
        help="Path to the output HDF5 file.",
    )

    args = vars(parser.parse_args())
    process_lhe_files(**args)


if __name__ == "__main__":
    main()
