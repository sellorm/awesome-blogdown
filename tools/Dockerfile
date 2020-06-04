FROM alpine:latest

RUN apk add python3 && pip3 install requests && mkdir -p /opt/sellorm

COPY ab200.py /opt/sellorm/

ENTRYPOINT ["/opt/sellorm/ab200.py"]
