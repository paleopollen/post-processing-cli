# Pollen Detection Post-processing Command Line Interface

We present Pollen Detection Post-processor, a Command Line Interface (CLI) for the post-processing of pollen detection
images generated using our Pollen Detection CLI (https://github.com/paleopollen/pollen-detection-cli). This CLI uses
the [Segment Anything Model 2](https://ai.meta.com/sam2/) (SAM 2) model to create segmentation masks and segmented
pollen images by using the center of pollen detection as the input prompt.

## Installation

## Download SAM 2 Checkpoints and Configuration Files

To download the SAM 2 checkpoints and configuration files, run the following commands:

```bash
cd checkpoints
./download.sh

cd sam2_configs
./download.sh
````

## Docker Build and Run

To install the package using Docker, run the following commands:

```bash
docker build -t palyim-post-processing-cli .

docker run -it --rm -v $(pwd)/data:/data -v $(pwd)/checkpoints:/usr/src/app/checkpoints -v $(pwd)/sam2_configs:/usr/src/app/sam2_configs palyim-post-processing-cli -d /data/pollen-detections-dir -m /usr/src/app/checkpoints/sam2_hiera_large.pt -c /usr/src/app/sam2_configs/sam2_hiera_l.yaml
```

Here, `-d` is the directory containing the pollen detection images, `-m` is the path to the SAM 2 model checkpoint, and
`-c` is the path to the SAM 2 configuration file. The output will be saved in the same directory as the input images.

## Usage

```shell
usage: post_processing_cli.py [-h] --detections-dir [DETECTIONS_DIR_PATH] --sam2-model-path [SAM2_MODEL_PATH] --sam2-config-path [SAM2_CONFIG_PATH]

Post process the pollen detection results.

options:
  -h, --help            show this help message and exit
  --detections-dir [DETECTIONS_DIR_PATH], -d [DETECTIONS_DIR_PATH]
                        Full path of the directory containing the detection results.
  --sam2-model-path [SAM2_MODEL_PATH], -m [SAM2_MODEL_PATH]
                        Full path of the SAM-2 model.
  --sam2-config-path [SAM2_CONFIG_PATH], -c [SAM2_CONFIG_PATH]
                        Full path of the SAM-2 config file.
```
