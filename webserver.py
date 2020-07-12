from flask import Response
from flask import Request
from flask import Flask
from flask import render_template
import Record
import cv2
import threading
import logging
import pyqrcode
import png
import config

lock = threading.Lock()


app = Flask(__name__)

def load_frame():
    """ Retrieve the most current frame from the record file and lock the thread to ensure no one else accesses simultaneously """
    while True:
            with lock:
                framedetect = Record.stream_frame()                  
            # wait until the lock is acquired
                if framedetect is None:
                    continue
                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", framedetect)
                # ensure the frame was successfully encoded
                if not flag:
                    continue
            # yield the output frame in the byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
        
@app.route("/")
def index():
    """ Load HTML file that has a placeholder for video_feed route"""
    return render_template("index.html")

def create_qr():
    """Create a QR code to access the video stream"""
    url = pyqrcode.create('http://172.20.10.3:5000/')
    streamQR = url.png("{}streamAccess.png".format(config.OUTPUT_PATH), scale=5)


@app.route("/video_feed")
def video_feed():
    """Load the frame into the html file"""
    # return the response generated along with the specific media
    # type (mime type)
    return Response(load_frame(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

def main():
    """ main function to set up a webserver and load the video stream to the server"""
    try:
        create_qr()
    except Exception as e:
        print(e)
        logging.debug(e)
            
    try:
        load_frame()
    except Exception as e:
        print(e)
        logging.debug(e)
    try:  
        app.run(threaded=True, use_reloader=False, port=config.PORT, host=config.HOST_ADDRESS)
    except Exception as e:
        print(e)
        logging.debug(e)
    
        
        

    
if __name__ == '__main__':
    main()

    
  