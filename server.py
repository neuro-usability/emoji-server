#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
# from machineLearning import createModel, predictEmoji

PORT_NUMBER = 3456
emojiList = {"derp": 12354, "herp": 34521}

# createModel()


#This class will handles any incoming request
class myHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		print("recieved POST request")
		length = int(self.headers['Content-Length'])
		receivedData = self.rfile.read(length).decode()
		print(receivedData)
		predictedEmoji = predictEmoji(receivedData)

		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.send_header("Access-Control-Allow-Origin", "*")
		self.end_headers()
		self.wfile.write(predictedEmoji)
		return
	#Handler for the GET requests
	# def do_GET(self):
	# 	self.send_response(200)
	# 	self.send_header('Content-type','application/json')
	# 	self.send_header("Access-Control-Allow-Origin", "*")
	# 	self.end_headers()
	# 	# emojiList = predictEmoji(clientData)
	# 	# print(123455)
	# 	self.wfile.write(json.dumps(emojiList).encode())
	# 	#self.send_response(200, "fuckyouuuu")
	# 	return


	# def do_POST(self):
    # # if None != re.search('/api/v1/addrecord/*', self.path):
    # #   ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    # #   if ctype == 'application/json':
	# 	print(self.rfile.read())
	# 	print("lolll")
    #     # length = int(self.headers.getheader('content-length'))
    #     # data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
    #     # recordID = self.path.split('/')[-1]
    #     # LocalData.records[recordID] = data
    #     # print "record %s is added successfully" % recordID
    # #   else:
    # #     data = {}
	# 	self.send_response(200)
	# 	self.end_headers()
    # # else:
    # #   self.send_response(403)
    # #   self.send_header('Content-Type', 'application/json')
    # #   self.end_headers()
    # return


try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()
