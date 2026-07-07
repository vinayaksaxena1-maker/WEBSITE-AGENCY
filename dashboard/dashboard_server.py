import os
import json
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from core.health_monitor import health_monitor
from agents.notification.notification_agent import NotificationAgent

class DashboardHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to suppress standard console logger spam
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read index.html
            html_path = os.path.join(os.path.dirname(__file__), 'index.html')
            with open(html_path, 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode('utf-8'))
                
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Run async health check in the sync handler context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                status = loop.run_until_complete(health_monitor.check_health())
            finally:
                loop.close()
                
            self.wfile.write(json.dumps(status).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/trigger':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Trigger Notification pipeline run
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                agent = NotificationAgent()
                mock_request = {
                    "request_identifier": "REQ-WEBUI-101",
                    "recipient_identifier": "admin@websiteagency.com",
                    "notification_type": "EMAIL",
                    "request_timestamp": "2026-07-07T00:00:00Z"
                }
                result = loop.run_until_complete(agent.execute_notification(mock_request))
            finally:
                loop.close()
                
            self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    server = HTTPServer(('localhost', port), DashboardHTTPHandler)
    print(f"Admin Dashboard Server is running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    run_server()
