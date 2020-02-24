import sys
import logging
import argparse
import os.path as pth
from collections import OrderedDict
from itertools import cycle
import numpy as np
from .io import load_approach
logging.basicConfig(format="%(levelname)-7s - %(name)s - %(message)s")
logger = logging.getLogger()


def export_plot(outfn, z, payload):
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    import matplotlib.pyplot as plt
    colors = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])
    fig = plt.figure()
    for i, (k, v) in enumerate(payload.items()):
        #plt.twinx()
        v_s = v-np.min(v)
        v_s /= np.max(v_s)
        lbl = f"{k} [{np.min(v):.02g}, {np.max(v):.02g}]"
        plt.plot(z, v_s, color=next(colors), label=lbl, zorder=-i)
        #plt.ylim(np.min(v), np.max(v))
    plt.xlim(np.min(z), np.max(z))
    logging.info(f"Saving to: {outfn}")
    plt.xlabel("Z (nm)")
    plt.legend(
        loc="upper left",
        handletextpad=1,
        handlelength=1,
        bbox_to_anchor=(1.0, 1.0),
    )
    plt.tight_layout()
    plt.savefig(outfn)

plot_exts = sorted([".png", ".svg", ".pdf"])
default_channels = ["M1A", "M1P", "O4A"]

all_exts = sorted(plot_exts)

parser = argparse.ArgumentParser(
    description="Load an approach curve and save or plot to another format.",
    epilog="Currently supported formats: "+" ".join(plot_exts)
    )
parser.add_argument("input", help="input file name")
parser.add_argument("-c", "--channels",
    action="extend",
    nargs="+",
    type=str,
    default=[],
    help="SNOM channels to use, separated by spaces. All channels are possible. Default: " + ", ".join(default_channels)
    )
parser.add_argument("-o", "--output", default=".png", help="output file name or extension. If it is an extension (ex: .png), will use the same base name. Default: '.png'")
parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity level")

args = parser.parse_args()
loglev = max(logger.level - 10*args.verbose, 10)
logger.setLevel(loglev)
logging.debug("arguments: "+str(args))
if not args.channels:
    args.channels = default_channels
if args.output.startswith("."):
    args.output = pth.splitext(args.input)[0] + args.output
logging.debug("output file name: "+args.output)

logging.info("Loading: "+args.input)
meta, data = load_approach(args.input)
z = data["Z"]*1E9 # use nm ffs
z -= np.min(z)
channels = OrderedDict()
for k in args.channels:
    try:
        channels[k] = data[k]
    except KeyError:
        logging.warn(f"Channel not in data: {k}")

if len(channels) == 0:
    choices = list(data.keys())
    logging.error("Fatal error: no correct channels found. Possible choices: "+", ".join(choices))
    sys.exit(1)

ext = pth.splitext(args.output)[1]
if ext in plot_exts:
    export_plot(args.output, z, channels)
else:
    logging.error(f"Output format not understood: {ext}. Possible choices: "+" ".join(all_exts))
    sys.exit(1)
