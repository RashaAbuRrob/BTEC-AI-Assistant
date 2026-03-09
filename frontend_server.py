#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/frontend')

PORT = 3000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🚀 Frontend server running at http://localhost:{PORT}")
    print(f"📱 Open your browser and go to: http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop the server")
    httpd.serve_forever()
