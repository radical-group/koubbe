FROM ubuntu:18.04

RUN apt-get update -y \
    && apt install python3 python3-pip python3-virtualenv -y

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install radical.entk

COPY ./facts/ ./home/facts

ENTRYPOINT ["/bin/bash"]