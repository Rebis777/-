from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.request

API_KEY = os.environ.get('API_KEY', '')
API_URL = os.environ.get('API_URL', 'http://localhost:11434/v1/chat/completions')

class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, HTTP-Referer, X-Title')
        self.end_headers()

    def do_POST(self):
        print(f"📥 Получен запрос на путь: {self.path}")
        if self.path == '/api/ai':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            headers = {'Content-Type': 'application/json'}
            if API_KEY:
                headers['Authorization'] = f'Bearer {API_KEY}'
            
            # Передаём заголовки от клиента (для OpenRouter)
            if 'HTTP-Referer' in self.headers:
                headers['HTTP-Referer'] = self.headers['HTTP-Referer']
            if 'X-Title' in self.headers:
                headers['X-Title'] = self.headers['X-Title']
            
            req = urllib.request.Request(
                API_URL,
                data=body,
                headers=headers,
                method='POST'
            )
            try:
                with urllib.request.urlopen(req) as response:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response.read())
                    print("✅ Успешно перенаправлено")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            print(f"⚠️ Неверный путь: {self.path}")
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    try:
        server = HTTPServer(('0.0.0.0', 8000), ProxyHandler)
        print('✅ Прокси-сервер запущен на http://localhost:8000')
        print(f'📡 API URL: {API_URL}')
        print('⏳ Ожидание запросов...')
        server.serve_forever()
    except OSError as e:
        print('❌ ОШИБКА: Порт 8000 уже занят!')
        print('Закройте другие окна командной строки и запустите снова.')
