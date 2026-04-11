#!/bin/zsh

circle_text() {
  local size=$1
  local output=$2

  # 1. High-precision math (restoring your precise multipliers)
  local psize=$(( size * 0.21484375 ))
  local radius=$(( size * 0.546875 ))

  # 2. Integer math for viewport string
  local v_size=$(( [##10] size ))
  local v_center=$(( [##10] size / 2 ))

  set -x
  magick \
    -background 'rgb(237,231,184)' \
    -font "Verdana" \
    -pointsize "$psize" \
    label:"continuous" \
    -trim +repage \
    -bordercolor 'rgb(237,231,184)' \
    -border $(( psize * 0.05 ))x$(( psize * 0.1 )) \
    -virtual-pixel Background \
    -distort Arc "360 90 $radius" \
    -define distort:viewport="${v_size}x${v_size}-${v_center}-${v_center}" \
    "override/$output"
}


# Relies on ImageMagick "convert" commmand

circle_text 512 pack.png

# Every size is scaled by 8 (note third arg of Arc)

circle_text 64 pack_thumb.png
