import json

from PIL import Image

import clip

src_dir = clip.directory('defaults', 'textures', 'block')
dst_dir = clip.directory('textures', 'block')

for prefix in ('', 'soul_', 'campfire_', 'soul_campfire_'):
    for suffix in ('', '_0', '_1'):
        file = f'{prefix}fire{suffix}.png'
        try:
            src = Image.open(f'{src_dir}/{file}').convert('RGBA')
            dst = Image.new('RGBA', src.size)
            size = src.size[0]
            half = int(size / 2)
            for frame_y in range(0, src.size[1], size):
                frame = src.crop((0, frame_y, size, frame_y + size))
                new_height = int(2 * size / 3)
                reduced = frame.resize((size, new_height))
                dst.paste(reduced, (0, frame_y + size - new_height))
            dst.save(f'{dst_dir}/{file}', optimize=True)

            mcmeta = json.load(open(f'{src_dir}/{file}.mcmeta'))
            mcmeta['animation']['frametime'] = 3
            json.dump(mcmeta, open(f'{dst_dir}/{file}.mcmeta', 'w'))
        except FileNotFoundError:
            print(f'skipping {file}')
