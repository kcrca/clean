#!/bin/zsh
set -x

places=(~/Library/Application\ Support/PrismLauncher/libraries/com/mojang/minecraft)
cd ~/clean/default_resourcepack

for f in $places; do
    loc="$f/$1/minecraft-$1-client.jar"
    if [ -f "$loc" ]; then
	echo $loc >/dev/tty
	rm -rf [a-df-z]*
	unzip -qq "$loc" -x '*.class' META-INF/'*'
	rm -f pack.*
	find */ -type f -print0 | xargs -0 chmod -w
	git add .
    else
	echo missing
	ls -l $loc
    fi
done
