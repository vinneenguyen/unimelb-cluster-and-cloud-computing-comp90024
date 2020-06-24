FROM python:latest

ARG OPENSTACKSDK_VER=0.46.0
ENV REQUESTS_VER=2.18.0

COPY [ "entrypoint.sh", "/" ]

RUN pip install openstacksdk==${OPENSTACKSDK_VER}; \
    chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
