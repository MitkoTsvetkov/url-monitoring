from flask import Response, Flask
import requests
import time
from prometheus_client import Gauge, generate_latest

app = Flask(__name__)

URLS = ["https://httpstat.us/503", "https://httpstat.us/200"]
url_up = Gauge('sample_external_url_up', 'URL Up Status', ['url'])
url_response_time = Gauge('sample_external_url_response_ms', 'URL Response Time (ms)', ['url'])

def check_urls():
    for url in URLS:
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            latency = (time.time() - start) * 1000
            url_response_time.labels(url=url).set(latency)
            url_up.labels(url=url).set(1 if response.status_code == 200 else 0)
        except Exception:
            url_response_time.labels(url=url).set(0)
            url_up.labels(url=url).set(0)

@app.route('/metrics')
def metrics():
    check_urls()
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)