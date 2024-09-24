# PALYIM Post-processing Command Line Interface

## Installation

Create a Python virtual machine and install the package using the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
``` 


## Download SAM 2 Checkpoints and Configuration Files

To download the SAM 2 checkpoints and configuration files, run the following commands:

```bash
cd checkpoints
./download.sh

cd sam2_configs
./download.sh
````

## Docker Installation

To install the package using Docker, run the following commands:

```bash

docker build -t palyim-post-processing-cli .

docker run -it --rm -v data:/data palyim-post-processing-cli -d /data/crops-test-4-detections_2024-07-25_23-15-34

docker run -it --rm -v $(pwd)/data:/data -v $(pwd)/checkpoints:/usr/src/app/checkpoints -v $(pwd)/sam2_configs:/usr/src/app/sam2_configs palyim-post-processing-cli -d /data/crops-test-4-detections_2024-07-25_23-15-34 -m checkpoints/sam2_hiera_large.pt -c sam2_configs/sam2_hiera_l.yaml

docker run -it --rm -v $(pwd)/data:/data -v $(pwd)/checkpoints:/usr/src/app/checkpoints palyim-post-processing-cli -d /data/crops-test-4-detections_2024-07-25_23-15-34 -m checkpoints/sam2_hiera_large.pt -c sam2_hiera_l.yaml 
```
