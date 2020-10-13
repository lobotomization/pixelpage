#!/bin/bash
CURVER="$1"
NEXTVER="$2"
echo "Copying $CURVER to $NEXTVER"
CURVER_FILES=(`find | grep $CURVER`)
for file in "${CURVER_FILES[@]}"
do
	cp -v  "$file" `echo "$file" | sed "s/$CURVER/$NEXTVER/"`
	find | grep $NEXTVER | xargs sed -i "s/$CURVER/$NEXTVER/"
done

cd pixelart
./addRoutes.sh $NEXTVER
cd ..
