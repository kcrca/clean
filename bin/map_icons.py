#!/usr/bin/env python3

__author__ = 'arnold'

from pathlib import Path

from PIL import Image

import clip

maps = {
    'abandoned_camp_map': 'abandoned_camp',
    'buried_ancient_city_map': 'ancient_city',
    'buried_mineshaft_map': 'mineshaft',
    'buried_treasure_map': 'red_x',
    'buried_trial_chambers_map': 'trial_chambers',
    'desert_pyramid_map': 'desert_pyramid',
    'desert_village_map': 'desert_village',
    'jungle_pyramid_map': 'jungle_temple',
    'ocean_monument_map': 'ocean_monument',
    'plains_village_map': 'plains_village',
    'savanna_village_map': 'savanna_village',
    'snowy_village_map': 'snowy_village',
    'swamp_hut_map': 'swamp_hut',
    'taiga_village_map': 'taiga_village',
    'warm_ocean_ruins_map': 'warm_ocean_ruins',
    'woodland_mansion_map': 'woodland_mansion',
}

decorations = Path(clip.directory('textures', 'map/decorations'))
icons = Path(clip.directory('textures', 'item'))
blank = Image.open(icons / 'map_template.png')

for map, dec in maps.items():
    dec_img = Image.open(decorations / f'{dec}.png')
    icon = blank.copy()
    clip.alpha_composite(icon, dec_img, (12, 12))
    icon.save(icons / f'{map}.png')
