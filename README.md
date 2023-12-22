# Http Jepegoptim

## Overview
This is a simple webserver that is used for JPEG compression. The server invokes jpegoptim under the hood and supports lossless and lossy compression.
The API automatically decides when to use progressive encoding bassed on the file size to produce the most optimal compression (see [here](https://superuser.com/questions/379404/what-is-the-difference-between-progressive-and-optimized-jpegs-in-photostop/897512#897512)).
In order to reduce the image size further it'll strip all metadata from the image.

## Usage
The api accepts PUT request with a file and the file name as a path. The request will perform lossless compression by stripping the metadata and optimize Huffman tables of the image.
```
curl -X PUT --upload-file <FILE_PATH> http://localhost:8000/%i.jpg --output <OUTPUT_PATH>
```

In case you want to do lossy compression just add `?quality=<VALUE>` query parameter and a value between 0 and 100.
```
curl -X PUT --upload-file <FILE_PATH> http://localhost:8000/%i.jpg?quality=90 --output <OUTPUT_PATH>
```

### Docker
Example of using docker-compose:
```
services:
  httpjpegoptiom:
    container_name: httpjepegoptim
    restart: unless-stopped
    build:
      context: .
      dockerfile: Dockerfile
    tmpfs:
      - /output
    ports:
      - 8000:8000
```

### NextCloud
This API can be used with NextCloud and [Workflow Script](https://github.com/nextcloud/workflow_script) to optimize the uploaded JPEG files. Just configure the workflow rules as you want and add the following script:
```
curl -X PUT --upload-file %f http://httpjepegoptim:8000/%i.jpg --output /data/%n
```

To preserve the timestamps of the original file you can use the following script which introduces temporary file:
```
touch -r %f /tmp/mtime_%i; curl -X PUT --upload-file %f http://httpjepegoptim:8000/%i.jpg --output /data/%n; touch -r /tmp/mtime_%i /data/%n
```

#### Credits
The http server is based on [this](https://gist.github.com/darkr4y/761d7536100d2124f5d0db36d4890109) example.