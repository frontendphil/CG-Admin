#!/bin/sh -f

for f in *.less
do
    file=$(basename $f)
    target=$(echo "$file" | sed -e "s/.less/.css/g")

    lessc "$file" > "../css/$target"
done