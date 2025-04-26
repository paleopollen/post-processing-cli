# A Command Line Interface for Basic Post-Processing of Pollen Detection Images Using Segment Anything Model 2 (SAM 2).

We present `Pollen Detection Post-processor`, a Command Line Interface (CLI) for basic post-processing of pollen
detection images generated using our [Pollen Detection CLI](https://github.com/paleopollen/pollen-detection-cli). This
CLI uses the [Segment Anything Model 2](https://ai.meta.com/sam2/) (SAM 2) model to create segmentation masks and
segmented pollen images by using the center of pollen detection as the input prompt.

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

### Build Docker Image

```bash
docker build -t post-processing-cli .
```

### Run CLI

Example command:

```bash
docker run -it --rm -v $(pwd)/data:/data -v $(pwd)/checkpoints:/usr/src/app/checkpoints -v $(pwd)/sam2_configs:/usr/src/app/sam2_configs post-processing-cli -d /data/pollen-detections-dir -m /usr/src/app/checkpoints/sam2_hiera_large.pt -c /usr/src/app/sam2_configs/sam2_hiera_l.yaml
```

Here, CLI arguments `-d` contains the path to the directory containing the pollen detection images, `-m` contains the
path to the SAM 2 model checkpoint, and `-c` contains the path to the SAM 2 configuration file. The CLI saves the output
segmentation masks and images in the same directory as the input detection images and updates the metadata JSON file.

An example directory structure for the input pollen detection images that uses the Pollen Detection CLI is as follows:

This example assumes 9 z-plane images with 256 pixels of overlap between each tile.

```
pollen-detections-dir
├── pollen_detection_slide1_0x_0y
│   ├── 0z.png
│   ├── 1z.png
│   ├── 2z.png
│   ├── 3z.png
│   ├── 4z.png
│   ├── 5z.png
│   ├── 6z.png
│   ├── 7z.png
│   ├── 8z.png
│   ├── mask_1.png
│   ├── metadata_1.json
├── pollen_detection_slide1_0x_768y
│   ├── 0z.png
│   ├── 1z.png
│   ├── 2z.png
│   ├── 3z.png
│   ├── 4z.png
│   ├── 5z.png
│   ├── 6z.png
│   ├── 7z.png
│   ├── 8z.png
│   ├── mask_1.png
│   ├── metadata_1.json
└── ...
```

## Usage

```shell
usage: post_processing_cli.py [-h] --detections-dir [DETECTIONS_DIR_PATH] --sam2-model-path [SAM2_MODEL_PATH] --sam2-config-path [SAM2_CONFIG_PATH]

Post-process the pollen detection results.

options:
  -h, --help            show this help message and exit
  --detections-dir [DETECTIONS_DIR_PATH], -d [DETECTIONS_DIR_PATH]
                        Full path of the directory containing the detection results.
  --sam2-model-path [SAM2_MODEL_PATH], -m [SAM2_MODEL_PATH]
                        Full path of the SAM-2 model.
  --sam2-config-path [SAM2_CONFIG_PATH], -c [SAM2_CONFIG_PATH]
                        Full path of the SAM-2 config file.
```
