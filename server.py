from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.request

API_KEY = os.environ.get('API_KEY', '')
API_URL = 'https://openrouter.ai/api/v1/chat/completions'

class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/ai':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            req = urllib.request.Request(
                API_URL,
                data=body,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {API_KEY}',
                    'HTTP-Referer': 'https://ваш-проект.onrender.com',
                    'X-Title': 'Furniture Constructor'
                },
                method='POST'
            )
            try:
                with urllib.request.urlopen(req) as response:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), ProxyHandler)
    print('Server running on port 8000')
    server.serve_forever()
