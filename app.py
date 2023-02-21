import http.server
import socketserver
import psycopg2

# Set the port number
PORT = 8080


# Define the handler to serve the output.html file with UTF-8 encoding
class server_handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            outputfile = 'output.html'
            self.path = f'/{outputfile}'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


handler = server_handler
handler.extensions_map[".html"] = "text/html; charset=utf-8"

# Create the server with the handler and port number
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving at http://127.0.0.1:{PORT}")
    # Serve the HTML file
    httpd.serve_forever()
