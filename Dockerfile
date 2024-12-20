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

RUN git clone https://github.com/facebookresearch/sam2.git \
    && cd sam2 \
    && git reset --hard c2ec8e14a185632b0a5d8b161928ceb50197eddc \
    && pip install -e . \
    && cd .. \
    && export SAM2_REPO_ROOT=/usr/src/app/sam2 \
    && export PYTHONPATH="${SAM2_REPO_ROOT}:${PYTHONPATH}"

COPY src/ /usr/src/app/post-processing-cli/

WORKDIR /usr/src/app/post-processing-cli/

ENTRYPOINT [ "python3", "post_processing_cli.py"]