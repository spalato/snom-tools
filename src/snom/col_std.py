#!python3
# python col_std.py infile.txt >> stds.csv

import sys
import logging
import argparse
import numpy as np
from os.path import splitext, basename
from snom.io.pg import load_raw

logging.basicConfig(format="%(levelname)-7s - %(name)s - %(message)s")
logger = logging.getLogger()

def load_txt(fn):
    with open(fn) as f:
        hdr = f.readline().strip().lstrip("# ").split()
    data = np.loadtxt(fn)
    return hdr, data

readers = {
    ".txt": load_txt,
    ".csv": load_raw,
}

parser = argparse.ArgumentParser(
    description="Computes standard deviations of the columns in a file.",
    epilog="Currently supported formats: "+" ".join(readers),
)

parser.add_argument("input", help="input file name")

args = parser.parse_args()

ext = splitext(args.input)[1]
hdr, data = readers[ext](args.input)
for n, v in zip(hdr, np.std(data, axis=0)):
    print(f"{args.input}, {n}, {v:.06e}")
