#!/bin/sh
# usage: sh main.py data/v1/scans

MATTERPORT_DATA_DIR=$1

for scanId in `ls $MATTERPORT_DATA_DIR`
do
    path="$MATTERPORT_DATA_DIR/$scanId/matterport_skybox_images"
    viewIds=""
    for file in `ls $path`:
    do
        arr=`echo $file | tr "_" "\n"`
        for x in $arr; do viewIds="$viewIds\n$x"; break; done
    done
    for viewId in `echo $viewIds | uniq`
        do
            echo "> " $scanId $viewId
            python3 create_image.py $scanId $viewId data/panorama
            echo "... done"
    done
done