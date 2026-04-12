#!/bin/zsh

circle_text() {
  local size=$1
  local output=$2
  local font=${3:-OPTIGaramond-Oldstyle}

  # 1. High-precision math (restoring your precise multipliers)
  local psize=$(( size * 0.21484375 ))
  local radius=$(( size * 0.546875 ))

  # 2. Integer math for viewport string
  local v_size=$(( [##10] size ))
  local v_center=$(( [##10] size / 2 ))

  set -x
  magick \
    -background 'rgb(237,231,184)' \
    -font "$font" \
    -pointsize "$psize" \
    label:"creamy" \
    -trim +repage \
    -virtual-pixel Background \
    -distort Arc "360 143 $radius" \
    -define distort:viewport="${v_size}x${v_size}-${v_center}-${v_center}" \
    "override/$output"
}


circle_text 512 pack.png
circle_text 64 pack_thumb.png
