# Bangladeshi Taka Note Detection API

A REST API for detecting and classifying Bangladeshi Taka banknotes using YOLOv11 object detection model.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Local Development](#local-development)
  - [Docker Deployment](#docker-deployment)
- [API Endpoints](#api-endpoints)
- [Model Details](#model-details)
- [Testing](#testing)
- [Performance](#performance)
- [Cloud Deployment](#cloud-deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

✅ **Real-time Detection**: Detect Bangladeshi Taka banknotes in images using YOLOv11
✅ **Denomination Classification**: Identify denominations (10, 20, 50, 100, 200, 500, 1000 Taka)
✅ **REST API**: FastAPI-based REST API with comprehensive endpoints
✅ **Batch Processing**: Process multiple images in a single request
✅ **Docker Support**: Pre-configured Dockerfile for containerized deployment
✅ **CORS Enabled**: Cross-Origin Resource Sharing enabled for web clients
✅ **Error Handling**: Comprehensive error handling and validation
✅ **Logging**: Built-in logging for debugging and monitoring
✅ **API Documentation**: Interactive API docs with Swagger UI and ReDoc

## Project Structure

```
Bangladeshi-Taka-Detection-API/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── classes.py              # Class names mapping
│   ├── predictor.py            # YOLO model inference
│   ├── schemas.py              # Pydantic data models
│   ├── utils.py                # Utility functions
│   ├── routes/
│   │   ├── __init__.py
│   │   └── predict.py          # API endpoints
│   └── services/
│       ├── __init__.py
│       └── detector.py         # Detection logic
├── model/
│   ├── README.txt
│   └── best.pt                 # YOLOv11 model weights (download required)
├── tests/
│   └── test_api.py             # API tests
├── uploads/                    # Temporary upload directory
├── outputs/                    # Output directory
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration (optional)
└── README.md                   # This file
```

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker and Docker Compose (for containerized deployment)
- GPU support (optional but recommended for faster inference)

## Installation

### 1. Clone the Repository

```bash
git clone <https://github.com/Ferdaus71/Bangladeshi-Taka-Detection-API>
cd Bangladeshi-Taka-Detection-API
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Model Weights

1. Download the trained YOLOv11 model weights (`best.pt`) from your training phase
2. Place the file in the `model/` directory

```bash
# Directory structure after placing model:
model/
├── README.txt
└── best.pt
```

## Configuration

Edit `app/config.py` to modify settings:

```python
# Model configuration
CONFIDENCE_THRESHOLD = 0.5       # Minimum confidence for detections
IOU_THRESHOLD = 0.45             # Intersection over Union threshold

# Upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # Maximum file size (10MB)
ALLOWED_EXTENSIONS = ["jpeg", "jpg", "png"]
```

## Usage

### Local Development

#### 1. Run the API Server

```bash
# Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using Python
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

#### 2. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Docker Deployment

#### 1. Build Docker Image

```bash
# Build the image
docker build -t bangladeshi-taka-detection:latest .

# Or with custom tag
docker build -t bangladeshi-taka-detection:v1.0 .
```

#### 2. Run Docker Container

```bash
# Run the container
docker run -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  bangladeshi-taka-detection:latest

# On Windows PowerShell:
docker run -p 8000:8000 `
  -v ${PWD}/uploads:/app/uploads `
  -v ${PWD}/outputs:/app/outputs `
  bangladeshi-taka-detection:latest
```

#### 3. Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

Run with Docker Compose:

```bash
docker-compose up -d
docker-compose logs -f  # View logs
```

## API Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response (200)**:
```json
{
  "status": "healthy",
  "service": "Bangladeshi Taka Detection API"
}
```

### 2. Root Endpoint

**GET** `/`

Get API information.

**Response (200)**:
```json
{
  "message": "Bangladeshi Taka Note Detection API Running Successfully",
  "version": "1.0.0",
  "endpoints": {
    "docs": "/docs",
    "redoc": "/redoc",
    "predict": "/predict",
    "predict_batch": "/predict-batch"
  }
}
```

### 3. Single Image Prediction

**POST** `/predict`

Detect Bangladeshi Taka notes in a single image.

**Request**:
- Content-Type: `multipart/form-data`
- Body: Image file (JPEG or PNG)

**Response (200)**:
```json
{
  "status": "success",
  "file_name": "sample.jpg",
  "detections_count": 3,
  "detections": [
    {
      "denomination": "100 Taka",
      "confidence": 0.9542,
      "bbox": [120.5, 95.3, 280.2, 210.7]
    },
    {
      "denomination": "500 Taka",
      "confidence": 0.8721,
      "bbox": [300.1, 50.2, 450.8, 190.5]
    }
  ]
}
```

**Error Responses**:

- **400 Bad Request**: Invalid file type or no file provided
- **500 Internal Server Error**: Processing error

### 4. Batch Prediction

**POST** `/predict-batch`

Detect notes in multiple images (max 10 files).

**Request**:
- Content-Type: `multipart/form-data`
- Body: Multiple image files

**Response (200)**:
```json
{
  "status": "batch_complete",
  "total_files": 3,
  "results": [
    {
      "file_name": "image1.jpg",
      "status": "success",
      "detections_count": 2,
      "detections": [...]
    },
    {
      "file_name": "image2.jpg",
      "status": "failed",
      "error": "Invalid file type"
    }
  ]
}
```

## Model Details

### YOLOv11 Configuration

- **Architecture**: YOLOv11 (Latest YOLO architecture)
- **Input Size**: 640x640 pixels
- **Classes**: 7 Bangladeshi Taka denominations
  - 10 Taka
  - 20 Taka
  - 50 Taka
  - 100 Taka
  - 200 Taka
  - 500 Taka
  - 1000 Taka

### Inference Pipeline

1. **Image Preprocessing**: Resize and normalize image
2. **Model Inference**: Run YOLOv11 detection
3. **Post-processing**: Filter by confidence threshold and NMS (Non-Maximum Suppression)
4. **Output Formatting**: Convert detections to JSON format

## Testing

### Unit Tests

```bash
# Run tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app
```

### Manual Testing with curl

#### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

#### Test Single Image Prediction

```bash
curl -X POST -F "file=@sample_image.jpg" http://localhost:8000/predict
```

#### Test Batch Prediction

```bash
curl -X POST \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  http://localhost:8000/predict-batch
```

### Testing with Postman

1. Open Postman
2. Create new request
3. Set method to **POST**
4. Set URL to `http://localhost:8000/predict`
5. Go to **Body** tab
6. Select **form-data**
7. Add key `file` with type **File**
8. Select an image file
9. Click **Send**

## Performance

### Expected Performance Metrics

- **Inference Time**: ~50-100ms per image (CPU), ~20-40ms (GPU)
- **Throughput**: ~10-20 images/second (CPU), ~25-50 images/second (GPU)
- **Model Size**: ~50MB
- **Memory Usage**: ~500MB (CPU), ~1GB (GPU)

### Optimization Tips

1. Use GPU for faster inference
2. Batch multiple images together
3. Adjust confidence threshold based on accuracy requirements
4. Use container with proper resource limits

## Cloud Deployment

### AWS EC2

```bash
# Connect to EC2 instance
ssh -i key.pem ubuntu@<instance-ip>

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
sudo apt-get install docker.io -y
sudo usermod -aG docker $USER

# Clone and deploy
git clone <https://github.com/Ferdaus71/Bangladeshi-Taka-Detection-API>
cd Bangladeshi-Taka-Detection-API
docker build -t taka-detection .
docker run -d -p 8000:8000 taka-detection
```

### Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Deploy

### Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`

## Troubleshooting

### Issue: Model not found

**Solution**: Ensure `model/best.pt` exists in the model directory

### Issue: CUDA not available

**Solution**: 
```bash
# Use CPU-only installation
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Issue: Port already in use

**Solution**:
```bash
# Use different port
uvicorn app.main:app --port 8001
```

### Issue: Out of Memory

**Solution**:
- Run on machine with more RAM
- Reduce batch size
- Use GPU

## Environment Variables

```bash
# Model configuration
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45

# Server configuration
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
```

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **ultralytics**: YOLO implementation
- **opencv-python**: Image processing
- **torch**: Deep learning framework
- **Pillow**: Image library
- **python-multipart**: File upload handling
- **pydantic**: Data validation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [API Documentation](#api-endpoints)
3. Check GitHub Issues

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Acknowledgments

- YOLOv11 by Ultralytics
- FastAPI framework
- The open-source community
