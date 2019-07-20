# -*- coding: utf-8 -*-
#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
import urllib, re, argparse, time, sys, requests
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT
from time import sleep

serial = spi(port=0, device=0, gpio=noop())

device = max7219(serial, cascaded=12, block_orientation=-90, rotate=2) 
    # "cascaded" equals the exact number of 16x16 max7219 "squares". 
    # The max7219 dot matrix leds are often (at least on eBay) sold with a pre-soldered configuration of 
    # 4 squares in a row (cascaded=4. If you daisy-chain 2 of those, you end up with "cascaded=8")
    # "block-orientation" is a convenient way of defining the output size/scroll direction/total display area. 
    # Any other parameters & options regarding the luma libraries are described in the documentation here:
    # [https://luma-led-matrix.readthedocs.io/en/latest/]
    
localtime = time.localtime(time.time())
ts = int(time.mktime(localtime))
ts2= str(ts)

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200) # status code 200 equals "OK"(-ish)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	# How to deal with GET requests
  def do_GET(self):
		self._set_headers()
		query = urlparse(self.path).query
		query_components = {}

    # The following section was the best I could come up with at the time, to make sure the web server
    # responded to requests containing parameter "led" only:
    
		if "led" in query:
			query_components = dict(qc.split("=") for qc in query.split("&"))
			msg = urllib.unquote(query_components["msg"])
			show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.03)
          # here you can add optional actions to perform whenever a new song is starting
          # (AKA whenever the "play/stop" status text/notification in iTunes or Spotify is changing)
      self.wfile.write("<html><body><h1>Led Alert is running</h1></body></html>")	# Whatever floats your boat... ⛵️
			
	def do_HEAD(self):
		self._set_headers()
	
  # How to deal with POST requests
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		self._set_headers()
		if self.path == '/led': 
			show_message(device, post_data, fill="white", font=proportional(LCD_FONT), scroll_delay=0.03)
			
def run(server_class=HTTPServer, handler_class=S, port=8181):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting Led Alert...'
	try:
		httpd.serve_forever()
  # Handler for closing/quitting properly on user key press (CTRL C).
  # However, it's only relevant/working if the script is NOT running in daemon/service mode. 
	except KeyboardInterrupt:
		pass
		httpd.server_close()
		print('\n Stopping Led Alert')

if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()
