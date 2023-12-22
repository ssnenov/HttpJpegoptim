#!/usr/bin/env python
import datetime
from http.server import SimpleHTTPRequestHandler
import os
import shutil
from urllib.parse import urlparse, parse_qs
try:
    import http.server as server
except ImportError:
    # Handle Python 2.x
    import SimpleHTTPServer as server

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to handle PUT requests"""
    def do_PUT(self: SimpleHTTPRequestHandler):
        """Save a file following a HTTP PUT request"""
        """Example: PUT /file.jpg?quality=90"""
        
        filename = os.path.join('/output', os.path.basename(self.path.split('?')[0]))
        queryString = parse_qs(urlparse(self.path).query)
        compressionQuality = (queryString.get("quality") or [None])[0]

        # Delete the file if already exists
        if os.path.exists(filename):
            os.remove(filename)

        file_length = int(self.headers['Content-Length'])
        read = 0
        with open(filename, 'wb+') as output_file:
            while read < file_length:
                new_read = self.rfile.read(min(66556, file_length - read))
                read += len(new_read)
                output_file.write(new_read)
            
        compressImage(filename, file_length, compressionQuality)

        self.send_response(200, 'OK')
        self.end_headers()

        with open(filename, 'rb') as file:
            shutil.copyfileobj(file, self.wfile)
        
        os.remove(filename)

def compressImage(filename, fileSize, quality):
    args = '--strip-all'
    if fileSize > 10000:
        args += ' --all-progressive'
    else:
        arggs += ' --all-normal'

    if quality:
        args += f' -m{quality}'

    os.system(f'jpegoptim "{filename}" {args}')

if __name__ == '__main__':
    server.test(HandlerClass=HTTPRequestHandler)