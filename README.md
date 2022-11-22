# Matterport3DSemSeg

Matterport3DSemSeg is a tool to create semantic segmentation masks from Matterport3D.

## Prerequisites

- Install [docker](https://docs.docker.com/engine/installation/)
- Install [nvidia-docker2.0](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0))
- [Matterport3DSimulator](https://github.com/peteanderson80/Matterport3DSimulator
  - Follow the instructions in the Matterport3DSimulator and go from ["Clone Repo"](https://github.com/peteanderson80/Matterport3DSimulator#clone-repo) to ["Dataset Preprocessing"](https://github.com/peteanderson80/Matterport3DSimulator#dataset-preprocessing).


## Instructions

### Preprocess

Execute the following code on Docker.

```
sh main.sh $MATTERPORT_DATA_DIR/v1/scans
```

### Create semantic segmentation masks


Execute the following code on the host. (Note that it is not on Docker)


```
pip install -r requirements.txt
```

```
python3 main.py
```


