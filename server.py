#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
from machineLearning import createModel, predictEmoji

PORT_NUMBER = 3456
emojiList = {"derp": 12354, "herp": 34521}

createModel()


#This class will handles any incoming request
class myHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		print("received POST request")
		length = int(self.headers['Content-Length'])
		print("    \n")
		receivedData = self.rfile.read(length);
		decodedData = json.loads(receivedData.decode("utf-8"))
		predictedEmoji = predictEmoji(decodedData)
		print("\npredicted emoji:", predictedEmoji)

		self.send_response(200)
		self.send_header('Content-type','text/plain')
		self.send_header("Access-Control-Allow-Origin", "*")
		self.end_headers()
		self.wfile.write(json.dumps(predictedEmoji.tolist()).encode())
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started HTTP server on port', PORT_NUMBER)

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()
