#!/bin/sh
# usage: sh main.py data/v1/scans

MATTERPORT_DATA_DIR=$1

for scanId in `ls $MATTERPORT_DATA_DIR`
do
    # prepare
    path="$MATTERPORT_DATA_DIR/$scanId/matterport_skybox_images"
    viewIds=""
    for file in `ls $path`:
    do
        arr=`echo $file | tr "_" "\n"`
        for x in $arr; do viewIds="$viewIds\n$x"; break; done
    done

    # create image
    for viewId in `echo $viewIds | uniq`
    do
        echo "> " $scanId $viewId
        python3 create_image.py $scanId $viewId data/panorama
        echo "... done"
    done
    
    # update ids.json
    echo "update ids.json"
    echo $viewIds | uniq | tr "\n" " " > .tmp
    python3 create_json.py ids.json $scanId
    rm .tmp
    echo "... done"
done