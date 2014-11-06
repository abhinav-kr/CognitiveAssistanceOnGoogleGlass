#!/usr/bin/env python
#
# Cloudlet Infrastructure for Mobile Computing
#
#   Author: Kiryong Ha <krha@cmu.edu>
#
#   Copyright (C) 2011-2013 Carnegie Mellon University
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import time
import Queue
import threading
import re
import sys
import json
#import pymatlab
#from pymatlab.matlab import MatlabSession
from pymatbridge import Matlab
from os import curdir
from os import sep
from BaseHTTPServer import BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from random import randint


import os
import sys
if os.path.isdir("../../gabriel"):
    sys.path.insert(0, "../..")
from gabriel.proxy.common import AppProxyStreamingClient
from gabriel.proxy.common import AppProxyThread
from gabriel.proxy.common import ResultpublishClient
from gabriel.proxy.common import get_service_list
from gabriel.common.config import ServiceMeta as SERVICE_META


share_queue = Queue.Queue();


class DummyVideoApp(AppProxyThread):
    def __init__(self, data_queue, output_queue_list,mlab):
	AppProxyThread.__init__(self, data_queue, output_queue_list)
	self.mlab = mlab

    def handle(self, header, data,):
	global share_queue
	global session
	offset = header['vm_offset']; 
	slice_perc =  header['vm_slice'];
	fidelity =  header['cog_eng_fidelity'];
    
        path_of_image = "/home/ivashish/tempImage.jpg"
        with open(path_of_image, 'wb') as file:
	        file.write(data)
        
	set_arg1 = "offset="+str(offset)+";"
	set_arg2 = "slice="+str(slice_perc)+";"
	set_arg3 = "fidelity="+str(fidelity)+";"

	mlab.run_code("addpath('/home/ivashish/exemplarsvm-master')")
	#results = mlab.run_func('detect_object_2.m',{'image_path':'/home/ivashish/tempImage.jpg','total_vm':total_vm,'vm_id':vm_id});
	mlab.run_code(set_arg1);
	mlab.run_code(set_arg2);
	mlab.run_code(set_arg3);
	results = mlab.run_code("detect_object_2('/home/ivashish/tempImage.jpg',offset,slice,fidelity)");
	ans = mlab.get_variable('ans')

	#import pdb; pdb.set_trace();	
	'''
	session = MatlabSession(matlab_root='/home/ivashish/Matlab')
	self.session.putvalue('x',3);
	ans = self.session.getvalue('x');
	'''
	'''
        matlab_session.putvalue('inputImagePath', path_of_image)
	matlab_session.run('addpath(genpath(\'/home/ishan/exemplarsvm-master\'))');
        matlab_session.run('results = detect_object(inputImagePath)')
 	ans= matlab_session.getvalue('results')
	'''
	#import pdb; pdb.set_trace()       
        
        share_queue.put_nowait(data)
	
        if not ans:
		ret = '';
	else:
		ret = 'bus found';

        return ret


class MJPEGStreamHandler(BaseHTTPRequestHandler, object):
    def do_GET(self):
        global share_queue
        self.data_queue = share_queue
        self.result_queue = Queue.Queue()

        try:
            self.path = re.sub('[^.a-zA-Z0-9]', "", str(self.path))
            if self.path== "" or self.path is None or self.path[:1] == ".":
                return
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith(".mjpeg"):
                self.send_response(200)
                self.wfile.write("Content-Type: multipart/x-mixed-replace; boundary=--aaboundary")
                self.wfile.write("\r\n\r\n")
                while 1:
                    if self.data_queue.empty() == False:
                        image_data = self.data_queue.get()
                        self.wfile.write("--aaboundary\r\n")
                        self.wfile.write("Content-Type: image/jpeg\r\n")
                        self.wfile.write("Content-length: " + str(len(image_data)) + "\r\n\r\n")
                        self.wfile.write(image_data)
                        self.wfile.write("\r\n\r\n\r\n")
                        time.sleep(0.001)
                return
            if self.path.endswith(".jpeg"):
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    stopped = False
    #class ThreadedHTTPServer(HTTPServer):
    """Handle requests in a separate thread."""
    def serve_forever(self):
        while not self.stopped:
            self.handle_request()

    def terminate(self):
        self.server_close()
        self.stopped = True

        # close all thread
        if self.socket != -1:
            self.socket.close()


if __name__ == "__main__":
    output_queue_list = list()

    sys.stdout.write("Finding control VM\n")
    service_list = get_service_list(sys.argv)
    video_ip = service_list.get(SERVICE_META.VIDEO_TCP_STREAMING_ADDRESS)
    video_port = service_list.get(SERVICE_META.VIDEO_TCP_STREAMING_PORT)
    acc_ip = service_list.get(SERVICE_META.ACC_TCP_STREAMING_ADDRESS)
    acc_port = service_list.get(SERVICE_META.ACC_TCP_STREAMING_PORT)
    return_addresses = service_list.get(SERVICE_META.RESULT_RETURN_SERVER_LIST)

    #session = pymatlab.session_factory();
    mlab = Matlab('/home/ivashish/Matlab/bin/matlab');
    mlab.start();

    # dummy video app
    image_queue = Queue.Queue(1)
    video_ip ='10.2.12.4'
    video_client = AppProxyStreamingClient((video_ip, video_port), image_queue)
    video_client.start()
    video_client.isDaemon = True
    app_thread = DummyVideoApp(image_queue, output_queue_list,mlab)
    app_thread.start()
    app_thread.isDaemon = True

    http_server = ThreadedHTTPServer(('0.0.0.0', 7070), MJPEGStreamHandler)
    http_server_thread = threading.Thread(target=http_server.serve_forever)
    http_server_thread.daemon = True
    http_server_thread.start()

    # result pub/sub
    result_pub = ResultpublishClient(return_addresses, output_queue_list)
    result_pub.start()
    result_pub.isDaemon = True

    try:
        while True:
            time.sleep(1)
    except Exception as e:
        pass
    except KeyboardInterrupt as e:
        sys.stdout.write("user exits\n")
    finally:
        video_client.terminate()
        app_thread.terminate()
        result_pub.terminate()

