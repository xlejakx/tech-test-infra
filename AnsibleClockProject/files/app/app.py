import os
import http.server
import socketserver
import signal
import sys
import time

PORT = int(os.environ.get("PORT", 80))
DIRECTORY = "."

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/clock':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            timestamp = str(time.time()).encode('utf-8')
            self.wfile.write(timestamp)
        else:
            super().do_GET()

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Server started at port {PORT}")

    def signal_handler(sig, frame):
        print("Server stopped.")
        httpd.server_close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
