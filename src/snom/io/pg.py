"""
snom.io.pg: Tools for loading exports from pyqtgraph.

"""
from os.path import splitext
import numpy as np
import logging
import pandas as pd
logger = logging.getLogger(__name__)

def is_partial_csv(fn):
    """Inspects the file to determine if it is a partial pg export."""
    root, ext = splitext(fn)
    if ext != ".csv":
        return False
    return root.split("_")[-1] in ["canti", "optical", "phase"]


def split_role(fn):
    """
    Splits the filename into 'root' and 'role' components.

    >> split_role("trial01_canti.csv")
    "trial01", "canti"
    """
    s = splitext(fn)[0].split("_")
    return "_".join(s[:-1]), s[-1]


# def load_raw_pg_csv(fname) -> pd.DataFrame:
#     """
#     Load csv from pyqtgraph. Returns a pandas DataFrame.
#     """
#     with open(fname) as f:
#         hdr = f.readline().strip().split(",")
#     hdr = [h.strip('"') for h in hdr]
#     data = np.loadtxt(fname, delimiter=",", skiprows=1, usecols=range(len(hdr)))
#     return pd.DataFrame(data, columns=hdr)

def load_phase(fn):
    with open(fn) as f:
        hdr = f.readline().strip().split(",")
    hdr = [h.strip('"')[:-2] for h in hdr]
    hdr[0] = "tap_p"
    return hdr, np.loadtxt(fn, delimiter=",", skiprows=1, usecols=range(len(hdr)))

def load_raw(fn):
    with open(fn) as f:
        hdr = f.readline().strip().split(",")[1:]
    hdr = [h.strip('"')[:-2] for h in hdr]
    return hdr, np.loadtxt(fn, delimiter=",", skiprows=1, usecols=range(1, len(hdr)+1))

def load_data(fn):
    logger.debug("Loading: "+fn)
    role = split_role(fn)[1]
    if role in ["canti", "optical"]:
        hdr, data = load_raw(fn)
    else:
        hdr, data = load_phase(fn)
    return pd.DataFrame(data, columns=hdr)

def is_num_idx(k):
    """This key corresponds to """
    return k.endswith("_x") and (k.startswith("tap_x") or k.startswith("sig"))


def cleanup(df: pd.DataFrame):
    cols = df.columns
    #logger.debug("Column names: " + ", ".join(cols.to_list()))
    dup = list(set(cols[cols.duplicated(keep=False)]))
    #logger.debug(repr(cols.duplicated(keep=False)))
    for k in dup:
        logger.debug("Duplicate key: "+k)
        sub = df.loc[:,k]
        logger.debug("subarray shape: "+repr(sub.shape))
        if not np.allclose(sub, sub.iloc[:,0][:,np.newaxis]):
            raise RuntimeError(f"Cannot drop duplicate key: {k}, some unequal values were found.")
    drop = cols.duplicated(keep="first")
    df = df.loc[:, ~drop]
    ORDER = ["sig_A", "sig_B", "sig_d", "sig_s", "tap_x", "tap_y", "tap_p"]
    reordered = sorted(df.columns.to_list(), key=ORDER.index)
    return df[reordered]
