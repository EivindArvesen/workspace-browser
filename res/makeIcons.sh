#!/usr/bin/env bash

# Must be run on a Mac. Depends on ImageMagick.

ICNFLD=icon.iconset


mkdir $ICNFLD
convert icon.png -resize 16x16 $ICNFLD/icon_16x16.png
convert icon.png -resize 32x32 $ICNFLD/icon_32x32.png
convert icon.png -resize 128x128 $ICNFLD/icon_128x128.png
convert icon.png -resize 256x256 $ICNFLD/icon_256x256.png
convert icon.png -resize 512x512 $ICNFLD/icon_512x512.png

cp $ICNFLD/icon_32x32.png $ICNFLD/icon_16x16@2x.png
cp $ICNFLD/icon_128x128.png $ICNFLD/icon_32x32@2x.png
cp $ICNFLD/icon_256x256.png $ICNFLD/icon_128x128@2x.png
cp $ICNFLD/icon_512x512.png $ICNFLD/icon_256x256@2x.png
convert icon.png -resize 1024x1024 $ICNFLD/icon_512x512@2x.png

cp $ICNFLD/icon_256x256.png small_icon.png

iconutil -c icns $ICNFLD
rm -rf $ICNFLD
