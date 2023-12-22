FROM alpine

EXPOSE 8000
VOLUME [ "/output" ]

COPY server.py server.py
RUN apk add --no-cache python3 jpegoptim

ENTRYPOINT [ "python3", "server.py" ]