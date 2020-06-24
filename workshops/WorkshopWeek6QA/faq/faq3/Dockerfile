FROM alpine:latest

WORKDIR /demo

RUN mkdir -p copy add1 add2

COPY ["release-1.18.0.tar.gz", "./copy/"]

ADD ["release-1.18.0.tar.gz", "./add1/"]

ADD ["https://github.com/nginx/nginx/archive/release-1.18.0.tar.gz", "./add2/"]
