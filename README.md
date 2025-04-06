# README.md

## URL Monitoring App (Prometheus Exporter)

This project is a simple Python service that checks the availability and response time of two external URLs:

- https://httpstat.us/200
- https://httpstat.us/503

It exposes metrics in a Prometheus-compatible format so they can be scraped and visualized via Grafana or used in alerting.

---

## What It Does

- Makes HTTP requests to the URLs listed above.
- Measures if the site is up (based on HTTP 200 status).
- Measures the response time in milliseconds.
- Exposes everything under the `/metrics` endpoint using Prometheus format.

---

## Technologies Used

- Python (Flask + prometheus-client + requests)
- Docker
- Kubernetes
- Helm

---

## Metrics Example

When you visit `/metrics`, you’ll see something like:

```
sample_external_url_up{url="https://httpstat.us/200"} 1
sample_external_url_response_ms{url="https://httpstat.us/200"} 48.37
sample_external_url_up{url="https://httpstat.us/503"} 0
sample_external_url_response_ms{url="https://httpstat.us/503"} 112.45
```

---

## How to Deploy This on Kubernetes

### 1. Build and Push the Docker Image

```bash
docker build -t yourusername/repo-name:your-tag .
docker push yourusername/repo-name:your-tag
```

### 2.Ajust Your `values.yaml` According your Configuration

```yaml
namespace: url-monitor

image:
  repository: yourusername/repo-name:your-tag
  tag: your-tag
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8000

serviceAccount:
  create: true
  name: ""
  annotations: {}

ingress:
  enabled: false

autoscaling:
  enabled: false
```

### 3. Deploy with Helm

```bash
cd helm
helm install url-monitor ./url-monitor \
  --create-namespace
```

### 4. Access the Metrics Endpoint

Once deployed, use port-forwarding to reach the service:

```bash
kubectl port-forward svc/url-monitor 8000:8000 -n url-monitor
```

Now you can visit [http://localhost:8000/metrics](http://localhost:8000/metrics)

---

## Clean Up

If you want to remove the app from your cluster:

```bash
helm uninstall url-monitor -n url-monitor
kubectl delete namespace url-monitor
```
