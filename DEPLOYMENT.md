# Deployment Guide - Bangladeshi Taka Detection API

This guide provides detailed instructions for deploying the Bangladeshi Taka Detection API on various platforms.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [AWS EC2 Deployment](#aws-ec2-deployment)
4. [Railway Deployment](#railway-deployment)
5. [Render Deployment](#render-deployment)
6. [Google Cloud Platform](#google-cloud-platform)
7. [Production Considerations](#production-considerations)

## Local Development

### Prerequisites

- Python 3.9+
- pip
- Git

### Setup Steps

1. **Clone Repository**
```bash
git clone <repository-url>
cd Bangladeshi-Taka-Detection-API
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Download Model Weights**
- Place your trained `best.pt` in the `model/` directory

5. **Run Development Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Access API**
- Swagger UI: http://localhost:8000/docs
- API: http://localhost:8000

## Docker Deployment

### Prerequisites

- Docker installed
- Docker Compose (optional)

### Build and Run

1. **Build Docker Image**
```bash
docker build -t bangladeshi-taka-detection:latest .
```

2. **Run Container**
```bash
docker run -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  bangladeshi-taka-detection:latest
```

3. **Run with Docker Compose**
```bash
docker-compose up -d
```

4. **Check Logs**
```bash
docker-compose logs -f api
```

5. **Stop Container**
```bash
docker-compose down
```

### Docker Commands Reference

```bash
# Build with custom tag
docker build -t my-registry/bangladeshi-taka-detection:v1.0 .

# Push to Docker Hub
docker push my-registry/bangladeshi-taka-detection:v1.0

# Run with environment variables
docker run -p 8000:8000 \
  -e CONFIDENCE_THRESHOLD=0.5 \
  -e IOU_THRESHOLD=0.45 \
  bangladeshi-taka-detection:latest

# Run with resource limits
docker run -p 8000:8000 \
  --memory=2g \
  --cpus=2 \
  bangladeshi-taka-detection:latest

# Inspect running container
docker ps
docker logs <container-id>
docker exec -it <container-id> bash
```

## AWS EC2 Deployment

### Prerequisites

- AWS Account
- EC2 instance (t2.medium or larger recommended)
- SSH access to the instance

### Deployment Steps

1. **Connect to EC2 Instance**
```bash
ssh -i your-key.pem ubuntu@<ec2-ip>
```

2. **Update System**
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

3. **Install Docker**
```bash
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
```

4. **Install Git**
```bash
sudo apt-get install -y git
```

5. **Clone Repository**
```bash
git clone <repository-url>
cd Bangladeshi-Taka-Detection-API
```

6. **Build and Run Docker Image**
```bash
docker build -t taka-detection:latest .
docker run -d -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  --restart unless-stopped \
  taka-detection:latest
```

7. **Configure Security Group**
- Go to AWS Console → EC2 → Security Groups
- Add inbound rule for port 8000
- Allow traffic from your IP or 0.0.0.0/0

8. **Access API**
```
http://<ec2-ip>:8000/docs
```

### Optional: Setup with Nginx Reverse Proxy

1. **Install Nginx**
```bash
sudo apt-get install -y nginx
```

2. **Create Nginx Configuration**
```bash
sudo nano /etc/nginx/sites-available/taka-detection
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

3. **Enable Configuration**
```bash
sudo ln -s /etc/nginx/sites-available/taka-detection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Railway Deployment

Railway is a modern platform for deploying applications.

### Prerequisites

- Railway Account
- Railway CLI installed
- GitHub repository

### Deployment Steps

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize Project**
```bash
railway init
```

4. **Configure Environment**
```bash
railway variables set PYTHONUNBUFFERED=1
```

5. **Deploy**
```bash
railway up
```

6. **View Logs**
```bash
railway logs
```

### Using GitHub Actions

1. **Connect GitHub Repository**
   - Go to Railway Dashboard
   - Create new project
   - Connect GitHub repo

2. **Set Build Command**
```
pip install -r requirements.txt
```

3. **Set Start Command**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

4. **Deploy**
   - Push changes to GitHub
   - Railway automatically deploys

## Render Deployment

Render is a modern cloud platform with free tier option.

### Prerequisites

- Render Account
- GitHub repository

### Deployment Steps

1. **Push Code to GitHub**
```bash
git push origin main
```

2. **Create New Web Service on Render**
   - Dashboard → New → Web Service
   - Connect GitHub repository
   - Select repository

3. **Configure Service**
   - **Name**: bangladeshi-taka-detection
   - **Region**: Choose nearest region
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**
   - Add any required environment variables
   - `PYTHONUNBUFFERED=1`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

6. **Access API**
```
https://<service-name>.onrender.com
```

## Google Cloud Platform

### Using Cloud Run

1. **Authenticate with GCP**
```bash
gcloud auth login
gcloud config set project <project-id>
```

2. **Build and Push Image**
```bash
gcloud builds submit --tag gcr.io/<project-id>/taka-detection
```

3. **Deploy to Cloud Run**
```bash
gcloud run deploy taka-detection \
  --image gcr.io/<project-id>/taka-detection \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

4. **Access Service**
```
https://<service-url>/docs
```

### Using Compute Engine (VM)

1. **Create VM Instance**
```bash
gcloud compute instances create taka-detection-vm \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --machine-type=e2-medium
```

2. **Connect to Instance**
```bash
gcloud compute ssh taka-detection-vm
```

3. **Setup (same as AWS EC2 steps above)**

## Production Considerations

### Security

1. **Use HTTPS**
   - Obtain SSL certificate (Let's Encrypt)
   - Configure Nginx or load balancer

2. **API Authentication**
```python
# Add to app.main.py
from fastapi.security import APIKey, APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/predict")
async def predict(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    # ... rest of function
```

3. **Rate Limiting**
```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(request: Request, file: UploadFile):
    # ...
```

4. **Input Validation**
   - Already implemented in routes
   - Validate file size
   - Sanitize inputs

### Performance

1. **Load Balancing**
   - Use load balancer (AWS ELB, GCP Load Balancer)
   - Scale horizontally with multiple instances

2. **Caching**
```python
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

# Configure Redis caching
```

3. **Database**
   - Use PostgreSQL for storing results
   - Implement result persistence

4. **Monitoring**
   - Use CloudWatch (AWS) or Stackdriver (GCP)
   - Setup alerts for errors
   - Monitor resource usage

### Monitoring and Logging

1. **Application Insights (Azure)**
```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()
```

2. **CloudWatch (AWS)**
```bash
pip install watchtower
```

3. **Datadog**
```bash
pip install datadog
```

### Health Checks

Ensure proper health check configuration:

```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### Database Backup

- Regular backup of logs and results
- Use cloud storage (S3, GCS)
- Implement disaster recovery

### Cost Optimization

1. **AWS**
   - Use spot instances for cost reduction
   - Auto-scaling groups
   - Reserved instances

2. **GCP**
   - Committed use discounts
   - Cloud Run auto-scaling

3. **Railway/Render**
   - Monitor usage
   - Optimize model size
   - Consider resource limits

## Troubleshooting Deployment

### Issue: Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <pid>
```

### Issue: Model Loading Timeout

```bash
# Increase timeout in deployment config
# For Railway/Render, adjust start command with timeout
```

### Issue: Out of Memory

```bash
# Check resource allocation
docker stats

# Increase memory limit
docker run --memory=4g ...
```

### Issue: Network Connectivity

```bash
# Test connection
curl http://localhost:8000/health

# Check firewall rules
# Check security group inbound rules
```

## Monitoring Checklist

- [ ] Health check endpoint working
- [ ] Logging configured
- [ ] Error alerts setup
- [ ] Performance metrics collected
- [ ] Backup strategy implemented
- [ ] Security measures in place
- [ ] Load testing completed
- [ ] Documentation updated

## Next Steps

1. Setup monitoring and logging
2. Configure backups
3. Implement caching
4. Add authentication if needed
5. Optimize for cost
6. Plan for scaling
7. Setup CI/CD pipeline

For additional help, refer to the main README.md
