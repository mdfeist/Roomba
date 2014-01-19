'''
	Roomba Server
'''

import cv2
import Image
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import StringIO
import time

import serial

capture = None
img = None

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print self.path
		if self.path == '/clean.html':
			if not ser.isOpen():
				ser.open()

			ser.isOpen()

			ser.write(chr(0x80))	# Start
			ser.write(chr(0x83))	# Safe
			ser.write(chr(0x87))	# Clean

			ser.close()
		if self.path == '/dock.html':
			if not ser.isOpen():
				ser.open()

			ser.isOpen()

			ser.write(chr(0x80))	# Start
			ser.write(chr(0x83))	# Safe
			ser.write(chr(0x8f))	# Dock

			ser.close()
		if self.path == '/cam.mjpg':
			self.send_response(200)
			self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					rc, img = capture.read()
					if not rc:
						print "Failed To Capture Image"
						continue
					imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
					cv2.imshow('frame', imgRGB)
					jpg = Image.fromarray(imgRGB)
					tmpFile = StringIO.StringIO()
					jpg.save(tmpFile, 'JPEG')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type', 'image/jpeg')
					self.send_header('Content-length', str(tmpFile.len))
					self.end_headers()
					jpg.save(self.wfile, 'JPEG')
					time.sleep(0.15)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://192.168.0.8:8000/cam.mjpg"/>')
			self.wfile.write('<br/><button onclick="location.href=\'/clean.html\'">Clean</button>')
			self.wfile.write('<br/><button onclick="location.href=\'/dock.html\'">Dock</button>')
			self.wfile.write('</body></html>')
			return



def main():
	global capture
	capture = cv2.VideoCapture(0)

	global img
	try:
		server = HTTPServer(('192.168.0.8', 8000), CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		capture.release()
		server.socket.close()


if __name__ == '__main__':
	main()
