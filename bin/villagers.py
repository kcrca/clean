#!/usr/bin/env python3
import configparser
import glob
import os
import re
import shutil

from PIL import Image

import clip

__author__ = 'arnold'

config = configparser.ConfigParser()
config.read(clip.directory('config', 'villagers.cfg'))

odds_re = re.compile(r'([^@]*)(?:@(\d+\.?\d*))?')
eyebrows_re = re.compile(r'(\d+)@(\d+),(\d+)')
hair_color_pos_re = re.compile(r'(\d+),(\d+)')

villager_dir = clip.directory('minecraft', 'optifine', 'random', 'entity', 'villager')
avatar_dir = os.path.join(villager_dir)
shutil.rmtree(avatar_dir, ignore_errors=True)
os.makedirs(avatar_dir)

for filename in glob.glob(f'{avatar_dir}/*'):
    os.unlink(filename)

people_config = config.items('people')

style_imgs = {}
skin_imgs = {}

os.chdir(clip.directory('textures', 'entity', 'villager'))

common_styles = config.get('settings', 'common_styles').split()

only_listed = set()
only_listed_desc = config.get('settings', 'only_listed')
if only_listed_desc:
    only_listed = set(only_listed_desc.split())

eyebrows = ()
eyebrows_desc = config.get('settings', 'eyebrows')
for eyebrow_desc in eyebrows_desc.split():
    m = eyebrows_re.match(eyebrow_desc)
    eyebrows += (tuple((int(v) for v in m.groups()), ),)

no_eyebrows = set(config.get('settings', 'no_eyebrows').split())

hair_color_pos = []
hair_color_desc = config.get('settings', 'hair_color').split()
for i in range(0, len(hair_color_desc)):
    m = hair_color_pos_re.match(hair_color_desc[i])
    hair_color_pos.append(tuple(int(v) for v in m.groups()))


def odds_for(descs):
    remaining = 1.0
    same = []
    odds = {}
    for desc in descs:
        thing, percent = odds_re.match(desc).groups()
        if percent:
            p = float(percent) / 100
            odds[thing] = p
            remaining -= p
        else:
            same.append(thing)
    for thing in same:
        odds[thing] = remaining / len(same)
    return odds


def build_avatars():
    avatar_num = 2
    villager_img = Image.open('parts/villager2.png')
    genotypes = [None, None]
    for skin_desc, hair_descs in people_config:
        skin, _ = odds_re.match(skin_desc).groups()
        if skin in skin_imgs:
            skin_img = skin_imgs[skin]
        else:
            skin_path = f'parts/{skin}.png'
            skin_img = skin_imgs[skin] = Image.open(skin_path).convert('RGBA')

        hair_for_skin = hair_descs.split()
        if skin not in only_listed:
            hair_for_skin += common_styles
        hairs = odds_for(hair_for_skin)
        for style in styles:
            for hair in hairs:
                if style == 'shaved':
                    genotype = f'{skin}_{style}'
                    hair_path = f'parts/hair_styles/hair_{style}.png'
                else:
                    genotype = f'{skin}_{hair}_{style}'
                    hair_path = f'parts/hair_styles/hair_{style}_{hair}.png'

                genotype_percent = skins[skin] * styles[style] * hairs[hair]
                # noinspection PyTypeChecker
                genotypes.append((genotype, genotype_percent))

                img = Image.alpha_composite(villager_img, skin_img)

                if (hair, style) in style_imgs:
                    hair_img = style_imgs[(hair, style)]
                else:
                    hair_img = style_imgs[(hair, style)] = Image.open(hair_path).convert('RGBA')
                # Special case for eyebrows
                eyebrow_handling(hair, hair_img, img, villager_img)
                img = Image.alpha_composite(img, hair_img)

                avatar_path = f'{avatar_dir}/villager{avatar_num:d}.png'
                img.save(avatar_path, optimize=True)
                avatar_num += 1

    return genotypes


def eyebrow_handling(hair, hair_img, img, villager_img):
    if hair not in no_eyebrows and eyebrows:
        hair_color = [0, 0, 0, 0]
        for color_pos in hair_color_pos:
            if hair_color[3] != 0:
                continue
            hair_color = hair_img.getpixel(color_pos)
        # Alpha is zero, so no real hair color
        if hair_color[3] != 0:
            eyebrow_color = clip.darker(hair_color[0:3]) + (hair_color[3],)
            for eyebrow in eyebrows:
                length, x, y = eyebrow
                for i in range(0, length):
                    # Need eyebrows only if the career image hasn't set the pixel
                    need_eyebrows = villager_img.getpixel((x, y))[3] == 0
                    if need_eyebrows:
                        img.putpixel((x + i, y), eyebrow_color)


styles = odds_for(config.get('settings', 'styles').split())
skins = odds_for(k for k, _ in people_config)

avatars = build_avatars()

prop_path = f'{avatar_dir}/villager.properties'
props = open(prop_path, 'w')

t = 0.0
weights = []
unemployed_textures = []
unemployed_weights = []
for i in range(0, len(avatars)):
    if avatars[i]:
        odds = avatars[i][1] * 100
        t += odds
        weight = odds * 100_000
        weights.append(f'{round(weight):d}')
        genotype = avatars[i][0]
        props.write(f'# {i:2d}: {odds:6.7f} {genotype}\n')
        if genotype.endswith('_dyed_default'):
            unemployed_textures.append(f'{i:d}')
            unemployed_weights.append(f'{weight:f}')
    else:
        assert i in (0, 1)

props.write(f'#     {t:6.3f}\n')
props.write('professions.1=none\n')
props.write(f'textures.1=1,{','.join(unemployed_textures)}\n')
props.write(f'weights.1=1,{','.join(unemployed_weights)}\n')
props.write(f'textures.2=1-{len(avatars) - 1:d}\n')
props.write(f'weights.2=1,{','.join(weights)}\n')
props.close()

profession_images = {}
shutil.copytree('parts/profession', f'{avatar_dir}/profession')
for file in sorted(glob.glob('parts/profession/*.png')):
    profession = os.path.basename(file)[:-5]
    if profession in profession_images:
        profession_images[profession].append(file)
    else:
        profession_images[profession] = [file]

for profession in profession_images:
    files = profession_images[profession]
    with open(f'{avatar_dir}/profession/{profession}.properties', 'w') as props:
        props.write(f'professions.1={profession}\n')
        props.write(f'textures.1=1-{len(files) + 1:d}\n')
        props.write(f'weights.1=0,{','.join((['100'] * len(files)))}\n')
