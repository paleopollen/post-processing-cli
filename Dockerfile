FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    python3-opencv \
    && mkdir -p /data \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN python3 -m venv .venv && . .venv/bin/activate

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/facebookresearch/segment-anything-2.git && cd segment-anything-2 && pip install -e . && cd ..

RUN export SAM2_REPO_ROOT=/usr/src/app/segment-anything-2
RUN export PYTHONPATH="${SAM2_REPO_ROOT}:${PYTHONPATH}"

COPY src/ /usr/src/app/

ENTRYPOINT [ "python3", "post_processing_cli.py"]