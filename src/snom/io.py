import numpy as np
import logging
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

