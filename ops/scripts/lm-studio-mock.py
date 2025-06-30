#!/usr/bin/env python3
"""
LM Studio Mock Server
Simulates LM Studio HTTP API with /v1/models and /v1/completions endpoints
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import sys

class MockLMStudioHandler(BaseHTTPRequestHandler):
    """HTTP handler for LM Studio API mock"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/v1/models':
            self._handle_models()
        else:
            self._send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/v1/completions':
            self._handle_completions()
        else:
            self._send_error(404, "Not Found")
    
    def _handle_models(self):
        """Return fake models list"""
        models_response = {
            "object": "list",
            "data": [
                {
                    "id": "llama-2-7b-chat",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "meta"
                },
                {
                    "id": "mistral-7b-instruct",
                    "object": "model", 
                    "created": int(time.time()),
                    "owned_by": "mistralai"
                }
            ]
        }
        
        self._send_json_response(models_response)
    
    def _handle_completions(self):
        """Return static completion response"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            request_body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(request_body) if request_body else {}
        except:
            request_data = {}
        
        # Check if streaming is requested
        stream = request_data.get('stream', False)
        
        if stream:
            self._handle_streaming_completion()
        else:
            completion_response = {
                "id": f"cmpl-{int(time.time())}",
                "object": "text_completion",
                "created": int(time.time()),
                "model": request_data.get("model", "llama-2-7b-chat"),
                "choices": [
                    {
                        "text": " Hello! This is a mock response from the LM Studio mock server.",
                        "index": 0,
                        "logprobs": None,
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": 5,
                    "completion_tokens": 12,
                    "total_tokens": 17
                }
            }
            
            self._send_json_response(completion_response)
    
    def _handle_streaming_completion(self):
        """Handle streaming SSE response"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Send streaming chunks
        chunks = ["Hello", " from", " mock", " server!"]
        
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "id": f"cmpl-{int(time.time())}",
                "object": "text_completion",
                "created": int(time.time()),
                "choices": [
                    {
                        "text": chunk,
                        "index": 0,
                        "finish_reason": None if i < len(chunks) - 1 else "stop"
                    }
                ]
            }
            
            self.wfile.write(f"data: {json.dumps(chunk_data)}\n\n".encode())
            self.wfile.flush()
            time.sleep(0.1)
        
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()
    
    def _send_json_response(self, data):
        """Send JSON response with CORS headers"""
        response_json = json.dumps(data, indent=2)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        self.wfile.write(response_json.encode())
    
    def _send_error(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_response = {"error": {"message": message, "code": code}}
        self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override to reduce log noise"""
        pass

def run_mock_server(port=1234):
    """Run the mock server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockLMStudioHandler)
    
    print(f"Mock LM Studio Server running on port {port}")
    print("Available endpoints:")
    print("  GET  /v1/models")
    print("  POST /v1/completions")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down mock server...")
        httpd.shutdown()

if __name__ == '__main__':
    port = 1234
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number")
            sys.exit(1)
    
    run_mock_server(port)
