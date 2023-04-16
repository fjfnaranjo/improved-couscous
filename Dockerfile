FROM python:3.9

RUN apt-get update && apt-get install -y \
    zip \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv

ADD requirements.txt /hello/
ADD requirements.py39runtime.txt /hello/
ADD requirements.dev.txt /hello/

RUN /venv/bin/pip install \
	-r /hello/requirements.txt \
	-r /hello/requirements.py39runtime.txt \
	-r /hello/requirements.dev.txt
