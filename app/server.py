import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "path"])
DURATION = Histogram("http_request_duration_seconds", "Request duration in seconds", ["method", "path"])
APP_INFO = Gauge("app_info", "Application version info", ["version"])
APP_INFO.labels(version="5.0.0").set(1)

class MetricsHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(generate_latest())
            return
        start = time.time()
        super().do_GET()
        DURATION.labels(method="GET", path=self.path).observe(time.time() - start)
        REQUESTS.labels(method="GET", path=self.path).inc()

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    server = HTTPServer(("0.0.0.0", 8080), MetricsHandler)
    server.serve_forever()
