import cv2
import sys
import time
import socket
import argparse
#from . import APP_NAME, APP_DESCRIPTION
from PIL import Image
from io import BytesIO
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import camera_zwo_asi
import datetime

capture = None
camera = camera_zwo_asi.Camera(0)
font = cv2.FONT_HERSHEY_PLAIN

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type',
                         'multipart/x-mixed-replace; boundary=--jpgboundary')
        self.end_headers()
        while True:
            try:
                #rc, img_bgr = capture.read()
                #if not rc:
                #    continue
                #img=cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)
                image = camera.capture()
                img = image.get_image()
                img = cv2.rotate(img, cv2.ROTATE_180)
                dt = datetime.datetime.now().strftime('BRTCam:  %d/%m/%Y %H:%M:%S WIB')
                img = cv2.putText(img, dt,
                            (20, 20),
                            font, 1,
                            (210, 155, 155),
                            1, cv2.LINE_8)
                jpg = Image.fromarray(img)
                tmpFile = BytesIO()
                jpg.save(tmpFile, 'JPEG')
                self.wfile.write(b'--jpgboundary\n')
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', str(sys.getsizeof(tmpFile)))
                self.end_headers()
                self.wfile.write(tmpFile.getvalue())
                time.sleep(0.5)
            except KeyboardInterrupt | BrokenPipeError:
                break


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    '''Handle requests in a separate thread.'''


class ThreadedHTTPServerV6(ThreadedHTTPServer):
    address_family = socket.AF_INET6


def main():
    global capture

    parser = argparse.ArgumentParser(
                                     allow_abbrev=False)
    parser.add_argument('--width',
                        type=int,
                        default=1920,
                        help='Web camera pixel width (default: 1920)')
    parser.add_argument('--height',
                        type=int,
                        default=1080,
                        help='Web camera pixel height (default: 1080)')
    parser.add_argument('--frame-rate', '--fps',
                        dest='fps',
                        default=60,
                        help='Frame rate of the webcam (default: 60)')
    parser.add_argument('--device',
                        dest='device',
                        type=str,
                        default='/dev/video0',
                        help='Path to the webcam device bus.'
                             ' (default: /dev/video0)')
    parser.add_argument('--host',
                        dest='host',
                        type=str,
                        default='0.0.0.0',
                        help='Host to bind server to (default: 0.0.0.0)')
    parser.add_argument('--port',
                        dest='port',
                        type=int,
                        default=8090,
                        help='Port listen on (default: 8090)')
    args = parser.parse_args()

    # Start the HTTP server
    try:
        server = ThreadedHTTPServer((args.host, args.port), CamHandler)
        print(f'Starting webcam server on http://{args.host}:{args.port}/')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopping server...')
        server.socket.close()


if __name__ == '__main__':
    main()
