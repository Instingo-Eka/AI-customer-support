from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 7860

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Customer Support Env is running!")

if __name__ == "__main__":
    print("Starting server...")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()