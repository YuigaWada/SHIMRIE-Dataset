#!/usr/bin/env python
'''
Script to create PNG format image, using 36 discretized views
at each viewpoint in 30 degree increments
'''

import math
import os
import sys
import numpy as np
from PIL import Image
import json

# Caffe and MatterSim need to be on the Python path
sys.path.append("Matterport3DSimulator/build")
import MatterSim

# Number of discretized views from one viewpoint
VIEWPOINT_SIZE = 36

# Simulator image parameters
WIDTH=640
HEIGHT=480
VFOV=60

def create_image(scanId, viewpointId, dir):
    """
    特定のviewpointについて、パノラマ画像を作成する。
    """
    # Set up the simulator
    sim = MatterSim.Simulator()
    sim.setCameraResolution(WIDTH, HEIGHT)
    sim.setCameraVFOV(math.radians(VFOV))
    sim.setDiscretizedViewingAngles(True)
    sim.setBatchSize(1)
    sim.initialize()

    state_list = []

    for ix in range(VIEWPOINT_SIZE):
        if ix == 0:
            sim.newEpisode([scanId], [viewpointId], [0], [math.radians(-30)])
        elif ix % 12 == 0:
            sim.makeAction([0], [1.0], [1.0])
        else:
            sim.makeAction([0], [1.0], [0])

        state = sim.getState()[0]
        state_dict = {
            'scanId': scanId,
            'viewpointId': viewpointId
        }
        state_dict['heading'] = state.heading
        state_dict['elevation'] = state.elevation
        state_dict['viewIndex'] = ix

        location_dict = {
            'ix': state.location.ix,
            'x': state.location.x,
            'y': state.location.y,
            'z': state.location.z,
            'rel_heading': state.location.rel_heading,
            'rel_elevation': state.location.rel_elevation,
            'rel_distance': state.location.rel_distance
        }

        state_dict['location'] = location_dict

        state_list.append(state_dict)

        assert state.viewIndex == ix

        array = np.array(state.rgb, copy=True)
        array = np.reshape(array, (480, 640, 3))
        array = array[:, :, ::-1]
        im = Image.fromarray(array)
        filename = "{}_{}_{:02d}.png".format(scanId, viewpointId, ix)
        im.save(os.path.join(dir, filename))

    json_dir = os.path.join('states')
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    with open(os.path.join(json_dir, "{}_{}_state.json".format(scanId, viewpointId)), 'w') as f:
        json.dump(state_list, f)



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("error: {} arguments passed. 3 arguments must be specified.".format(len(sys.argv) - 1))
        print("usage: \n    {} scanId viewpointId output_path".format(os.path.basename(__file__)))
        sys.exit(1)

    create_image(sys.argv[1], sys.argv[2], sys.argv[3])
