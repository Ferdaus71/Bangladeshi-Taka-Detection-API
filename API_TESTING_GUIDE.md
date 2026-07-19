# API Testing Guide

Complete guide for testing the Bangladeshi Taka Detection API.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Testing with curl](#testing-with-curl)
3. [Testing with Postman](#testing-with-postman)
4. [Testing with Python](#testing-with-python)
5. [Automated Testing](#automated-testing)
6. [Performance Testing](#performance-testing)
7. [Debugging](#debugging)

## Prerequisites

- Running API server (http://localhost:8000)
- Test images (JPEG or PNG format)
- Optional: curl, Postman, or Python installed

## Testing with curl

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Bangladeshi Taka Detection API"
}
```

### 2. API Information

```bash
curl http://localhost:8000/
```

### 3. Single Image Prediction

```bash
curl -X POST -F "file=@/path/to/image.jpg" \
  http://localhost:8000/predict
```

Example with a test image:
```bash
curl -X POST -F "file=@test_image.jpg" \
  http://localhost:8000/predict | python -m json.tool
```

### 4. Batch Prediction

```bash
curl -X POST \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  http://localhost:8000/predict-batch | python -m json.tool
```

### 5. Error Testing

Test with invalid file type:
```bash
# Create a text file
echo "This is not an image" > test.txt

# Try to upload
curl -X POST -F "file=@test.txt" \
  http://localhost:8000/predict
```

Expected error:
```json
{
  "detail": "Invalid file type: text/plain. Only JPEG and PNG images are allowed."
}
```

## Testing with Postman

### Import Postman Collection

1. **Open Postman**
2. **Click Import** → Choose "Import from Link"
3. **Paste URL** or import the collection file

### Manual Setup

#### Create Collection

1. File → New Collection
2. Name: "Bangladeshi Taka Detection API"

#### Add Requests

##### Request 1: Health Check

- **Method**: GET
- **URL**: `http://localhost:8000/health`
- **Expected Status**: 200

##### Request 2: API Info

- **Method**: GET
- **URL**: `http://localhost:8000/`
- **Expected Status**: 200

##### Request 3: Single Prediction

- **Method**: POST
- **URL**: `http://localhost:8000/predict`
- **Body**: 
  - Type: `form-data`
  - Key: `file` (File type)
  - Value: Select your test image
- **Expected Status**: 200

##### Request 4: Batch Prediction

- **Method**: POST
- **URL**: `http://localhost:8000/predict-batch`
- **Body**:
  - Type: `form-data`
  - Key: `files` (File type)
  - Value: Select multiple images
- **Expected Status**: 200

### Test Response Validation

1. **Go to Tests tab**
2. **Add validation script**:

```javascript
pm.test("Status code is 200", function() {
    pm.response.to.have.status(200);
});

pm.test("Response has detections", function() {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('detections');
});

pm.test("Detection has required fields", function() {
    var jsonData = pm.response.json();
    jsonData.detections.forEach(function(detection) {
        pm.expect(detection).to.have.property('denomination');
        pm.expect(detection).to.have.property('confidence');
        pm.expect(detection).to.have.property('bbox');
    });
});
```

## Testing with Python

### Simple Test

```python
import requests

# Health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# Single prediction
with open('test_image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f}
    )
print(response.json())
```

### Comprehensive Test Script

```python
import requests
import json
from pathlib import Path

class APITester:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self):
        """Test health endpoint"""
        response = self.session.get(f'{self.base_url}/health')
        print(f"Health: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    
    def test_predict(self, image_path):
        """Test prediction endpoint"""
        with open(image_path, 'rb') as f:
            response = self.session.post(
                f'{self.base_url}/predict',
                files={'file': f}
            )
        print(f"Predict: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    
    def test_batch(self, image_paths):
        """Test batch prediction"""
        files = [('files', open(p, 'rb')) for p in image_paths]
        response = self.session.post(
            f'{self.base_url}/predict-batch',
            files=files
        )
        for _, f in files:
            f.close()
        print(f"Batch: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200

# Usage
tester = APITester()
tester.test_health()
tester.test_predict('test_image.jpg')
tester.test_batch(['img1.jpg', 'img2.jpg'])
```

## Automated Testing

### Run Test Suite

```bash
# Run all tests
python tests/test_api.py

# With pytest
pytest tests/test_api.py -v

# With coverage
pytest tests/test_api.py --cov=app
```

### Continuous Testing

```bash
# Watch for changes and re-run tests
pytest-watch tests/

# Or use pytest directly
pytest tests/test_api.py -v --tb=short --looponfail
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Single request
ab -n 100 -c 10 http://localhost:8000/health

# With POST data
ab -n 100 -c 10 -p data.json http://localhost:8000/predict
```

### Load Testing with Locust

Install Locust:
```bash
pip install locust
```

Create `locustfile.py`:
```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def health_check(self):
        self.client.get('/health')
    
    @task
    def predict(self):
        with open('test_image.jpg', 'rb') as f:
            self.client.post('/predict', files={'file': f})
```

Run tests:
```bash
locust -f locustfile.py --host=http://localhost:8000
```

### Benchmark Results

Test configuration:
- Requests: 100
- Concurrency: 10
- Image size: ~500KB

Expected results (CPU i7-10700K):
- RPS: ~10-20
- Avg response time: 50-150ms
- Success rate: >99%

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check API Logs

```bash
# If running with Docker
docker logs <container-id> -f

# If running locally
# Check console output
```

### Test Invalid Inputs

```bash
# Missing file
curl -X POST http://localhost:8000/predict

# Wrong file type
curl -X POST -F "file=@document.pdf" http://localhost:8000/predict

# Too large file
curl -X POST -F "file=@large_file.jpg" http://localhost:8000/predict

# Wrong filename format
curl -X POST http://localhost:8000/predict
```

### Response Analysis

Check the response structure:

```python
response = requests.post(...)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"Body: {response.text}")
print(f"JSON: {response.json()}")
```

## Test Scenarios

### Scenario 1: Single Banknote Detection

1. Upload image with one banknote
2. Verify:
   - Status: 200
   - detections_count: 1
   - confidence > 0.7

### Scenario 2: Multiple Banknotes

1. Upload image with 3-5 banknotes
2. Verify:
   - Status: 200
   - detections_count: 3-5
   - All detections have confidence scores

### Scenario 3: No Banknotes

1. Upload image without banknotes
2. Verify:
   - Status: 200
   - detections_count: 0
   - detections: []

### Scenario 4: Partial Detection

1. Upload image with banknote partially in frame
2. Verify:
   - Status: 200
   - Detection returned (if confidence high enough)
   - Bounding box coordinates reasonable

### Scenario 5: Error Handling

1. Upload invalid file type
2. Verify:
   - Status: 400
   - Error message clear

## Expected Response Examples

### Successful Response

```json
{
  "status": "success",
  "file_name": "banknotes.jpg",
  "detections_count": 2,
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

### No Detections

```json
{
  "status": "success",
  "file_name": "image.jpg",
  "detections_count": 0,
  "detections": []
}
```

### Error Response

```json
{
  "detail": "Invalid file type: text/plain. Only JPEG and PNG images are allowed."
}
```

## Tips & Tricks

1. **Save responses for analysis**
   ```bash
   curl -X POST -F "file=@image.jpg" http://localhost:8000/predict > response.json
   ```

2. **Use jq for JSON formatting**
   ```bash
   curl -X POST -F "file=@image.jpg" http://localhost:8000/predict | jq '.'
   ```

3. **Measure response time**
   ```bash
   curl -w "@curl-format.txt" -X POST -F "file=@image.jpg" http://localhost:8000/predict
   ```

4. **Test with Python requests**
   ```python
   import requests
   r = requests.post('http://localhost:8000/predict', files={'file': open('image.jpg', 'rb')})
   r.elapsed.total_seconds()  # Response time in seconds
   ```

## Checklist

- [ ] Health endpoint returns 200
- [ ] API info endpoint works
- [ ] Single image prediction works
- [ ] Batch prediction works
- [ ] Error handling for invalid files
- [ ] Error handling for missing files
- [ ] Response format is correct
- [ ] Confidence scores are reasonable
- [ ] Bounding boxes are valid
- [ ] Performance is acceptable

For more information, see [README.md](README.md) and [API_ENDPOINTS.md](README.md#api-endpoints)
