from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.request

class ProxyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/ai':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            
            req = urllib.request.Request(
                'http://localhost:11434/v1/chat/completions',
                data=body,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            try:
                with urllib.request.urlopen(req) as response:
                    result = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(result)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), ProxyHandler)
    print('Сервер запущен на http://localhost:8000')
    server.serve_forever()