# Quick Start Guide

Get the Bangladeshi Taka Detection API running in 5 minutes!

## Prerequisites

- Python 3.9+ OR Docker
- Model weights file (best.pt)

## Option 1: Local Setup (5 minutes)

### Step 1: Download and Setup

```bash
# Clone repository
git clone <your-repo-url>
cd Bangladeshi-Taka-Detection-API

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Add Model Weights

```bash
# Copy your trained model to the model directory
cp /path/to/best.pt model/best.pt
```

### Step 3: Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

### Step 4: Test the API

Open your browser and go to:
```
http://localhost:8000/docs
```

## Option 2: Docker Setup (5 minutes)

### Step 1: Add Model Weights

```bash
cp /path/to/best.pt model/best.pt
```

### Step 2: Build and Run

```bash
# Build Docker image
docker build -t taka-detection:latest .

# Run container
docker run -p 8000:8000 taka-detection:latest
```

### Step 3: Test the API

Open your browser and go to:
```
http://localhost:8000/docs
```

## Quick Test

### Using curl

```bash
# Test health
curl http://localhost:8000/health

# Test with image
curl -X POST -F "file=@test_image.jpg" http://localhost:8000/predict
```

### Using Python

```python
import requests

# Predict on image
with open('test_image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f}
    )

print(response.json())
```

### Using Postman

1. **Create new request**
   - Method: POST
   - URL: http://localhost:8000/predict

2. **Setup body**
   - Go to "Body" tab
   - Select "form-data"
   - Add key: "file" (type: File)
   - Select your test image

3. **Send and see results**

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/predict` | Single image prediction |
| POST | `/predict-batch` | Batch prediction (max 10 images) |

## Response Format

### Successful Response (200)

```json
{
  "status": "success",
  "file_name": "image.jpg",
  "detections_count": 2,
  "detections": [
    {
      "denomination": "100 Taka",
      "confidence": 0.9542,
      "bbox": [120.5, 95.3, 280.2, 210.7]
    }
  ]
}
```

### Error Response (400/500)

```json
{
  "detail": "Error message"
}
```

## Common Issues

### Issue: Model not found

```
Error: Model file not found at model/best.pt
```

**Solution**: Place your model file in the `model/` directory

### Issue: Port already in use

```
Error: Address already in use
```

**Solution**: 
```bash
# Use different port
uvicorn app.main:app --port 8001
```

### Issue: Import errors

```
ModuleNotFoundError: No module named 'torch'
```

**Solution**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Next Steps

1. **Learn the API**
   - Read [README.md](README.md) for detailed documentation
   - Check [MODEL_GUIDE.md](MODEL_GUIDE.md) for model information

2. **Deploy to Production**
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment options
   - Docker Compose setup for production

3. **Testing**
   - Run comprehensive tests: `python tests/test_api.py`
   - Use provided test images

4. **Optimization**
   - Adjust confidence thresholds
   - Fine-tune model if needed
   - Setup GPU acceleration

## Configuration

Edit `app/config.py` to customize:

```python
# Model parameters
CONFIDENCE_THRESHOLD = 0.5  # Lower = more detections
IOU_THRESHOLD = 0.45        # Lower = fewer overlaps

# API settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max
```

## Docker Commands

```bash
# View logs
docker logs <container-id>

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# Access shell
docker exec -it <container-id> bash
```

## Useful Links

- 📖 [Full Documentation](README.md)
- 🚀 [Deployment Guide](DEPLOYMENT.md)
- 🤖 [Model Guide](MODEL_GUIDE.md)
- 📊 [API Documentation](http://localhost:8000/docs)
- 🐛 [Troubleshooting](README.md#troubleshooting)

## Support

Having issues? Check out:
1. [Troubleshooting section](README.md#troubleshooting)
2. GitHub Issues
3. Model documentation in [MODEL_GUIDE.md](MODEL_GUIDE.md)

---

**Happy detecting! 🎉**

Next: Read [README.md](README.md) for comprehensive documentation.
