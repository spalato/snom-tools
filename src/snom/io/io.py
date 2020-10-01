import numpy as np
import logging
import os.path as pth
from deprecated import deprecated
logger = logging.getLogger(__name__)

@deprecated("Function renamed to `load_approach`")
def load_curve(*args):
    return load_approach(*args)


def load_approach(fn):
    with open(fn, encoding="utf-8") as f:
        meta = []
        for l in f:
            if l.startswith("#"):
                meta.append(l)
            else:
                hdr = l
                break
    hdr = hdr.split()
    dat = np.loadtxt(fn, skiprows=len(meta)+1)
    assert dat.shape[1] == len(hdr)
    return "".join(meta), dict(zip(hdr, dat.T))


def load_scope(*fnames):
    """Load a series of csv files exported from the scope.

    Collects them in a single (x,y,y) series. Returns the channel names.
    """
    channels = [pth.split(fn)[-1][:2] for fn in fnames]
    data = [np.loadtxt(fn, delimiter=",", skiprows=5) for fn in fnames]
    x = [d[:,0] for d in data]
    if not np.allclose(np.array(x), x[0].reshape((1,-1))):
        raise ValueError("Misaligned x axis. The first column must match for all files")
    return channels, np.vstack([x[0]]+[d[:,1] for d in data]).transpose()
