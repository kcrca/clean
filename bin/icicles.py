#!/usr/bin/env python3

__author__ = 'arnold'

import shutil
from pathlib import Path

import glob

from bin import clip

# This is just a hack, because icicle file names are just different. This relies on the appropriate `colorize` command
# to first create the right image files. This then simply handles the naming inconsistency.

dir = Path(clip.directory('textures', 'block'))
for f in glob.glob(str(dir / 'icicle_down_*.png')):
    # print(f, str(f).replace('_down', ''))
    shutil.move(f, str(f).replace('_down', ''))