"""
OIt files are usually copies of the non-oit variants, this just copies those.
"""
from pathlib import Path

import clip

src_blocks = Path(clip.directory('defaults', 'textures', 'block'))
dst_blocks = Path(clip.directory('textures', 'block'))
for src in src_blocks.glob(f'*_oit*.png'):
    plain = dst_blocks / src.name.replace('_oit', '')
    if plain.is_file():
        dst = dst_blocks / src.name
        plain.copy(dst)
