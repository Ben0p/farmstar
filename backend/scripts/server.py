from http.server import BaseHTTPRequestHandler, HTTPServer
import nmea

server = {'Status':'',
          'Response':'',
          'IP':'',
          'Port':'',
          }

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        # Send message back to client
        message = '{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (nmea.GGA['Latitude'],  nmea.GGA['Longitude'])
        # Write content as utf-8 data
        response = self.wfile.write(bytes(message, "utf8"))
        server['Response'] = response
        return
 
def run():
  server['Status'] = "Starting"
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  server['Status'] = "Running"
  httpd.serve_forever()
 
 
run()
