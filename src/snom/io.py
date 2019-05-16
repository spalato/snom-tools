# snom.io: read and write
import numpy as np
import logging
logger = logging.getLogger(__name__)

def load_curve(fn):
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
