#!/usr/bin/env python


'''
face detection using haar cascades in remote fashion
'''

from __future__ import print_function
import urllib
import sys
from flask import Flask, render_template, Response, g,request
from detect_haar import face_detect
from cv_decoder import *
from cv_jpgencoder import *
from cv_haar_processor import *

app = Flask(__name__)

@app.route('/edge')
def indexEdge():
	quality = request.args.get('q')
   	if quality is None:
        	quality = 100
    	return render_template('indexEdge.html', quality=quality)


@app.route('/cloud')
def indexCloud():
 	quality = request.args.get('q')
   	if quality is None:
        	quality = 100
    	return render_template('indexCloud.html', quality=quality)



	
@app.route('/decode')
def decode():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)
    from flask import stream_with_context
    return Response(stream_with_context(cv_decode(stream)))

@app.route('/jpgencode')
def jpgencode():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)

    return Response(jpgencodestream(stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/serve_face')
def serve_face():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)

    return Response(face_detect_process(stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def video():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)
    return Response(face_detect(stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(host='169.254.250.163', port=port, debug=True)
