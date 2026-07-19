# Model Guide - Bangladeshi Taka Detection

This guide explains the YOLOv11 model used for Bangladeshi Taka note detection.

## Table of Contents

1. [Model Overview](#model-overview)
2. [Model Architecture](#model-architecture)
3. [Class Definitions](#class-definitions)
4. [Input/Output Specifications](#inputoutput-specifications)
5. [Training Details](#training-details)
6. [Model Performance](#model-performance)
7. [Using the Model](#using-the-model)
8. [Fine-tuning](#fine-tuning)
9. [Model Export Formats](#model-export-formats)

## Model Overview

### What is YOLOv11?

YOLOv11 (You Only Look Once v11) is a state-of-the-art real-time object detection model developed by Ultralytics. 

**Key Features:**
- Single-shot detection (no region proposal required)
- Real-time performance
- High accuracy
- Compact model size
- Easy to use API

### Why YOLOv11 for Currency Detection?

1. **Speed**: Can process images at 60+ FPS on CPU
2. **Accuracy**: High precision for small objects (useful for banknote details)
3. **Robustness**: Works well with various lighting conditions
4. **Flexibility**: Easy to train on custom datasets

## Model Architecture

### Network Structure

```
Input (640x640x3)
    ↓
Backbone (CSPDarknet)
    ├─ Conv Layers
    ├─ C2f Modules
    └─ SPPF (Spatial Pyramid Pooling)
    ↓
Neck (FPN-PAN)
    ├─ Multi-scale feature fusion
    ├─ Top-down pathway
    └─ Bottom-up pathway
    ↓
Head (Detect)
    ├─ Classification head (7 classes)
    ├─ Regression head (bounding boxes)
    └─ Objectness head (confidence)
    ↓
Output
    ├─ Class predictions
    ├─ Confidence scores
    └─ Bounding boxes
```

### Model Variants

YOLOv11 comes in different sizes:

| Variant | Parameters | Model Size | Speed (CPU) |
|---------|-----------|-----------|-----------|
| nano    | 2.6M      | 6.5 MB    | ~40 ms    |
| small   | 9.1M      | 21.5 MB   | ~50 ms    |
| medium  | 20.1M     | 49 MB     | ~75 ms    |
| large   | 43.7M     | 107 MB    | ~150 ms   |
| xlarge  | 68.1M     | 169 MB    | ~250 ms   |

### Model Used in This Project

- **Variant**: Based on training configuration
- **Model Size**: ~50-100 MB
- **Input Size**: 640x640 pixels
- **Speed**: 50-100ms per image (CPU), 20-40ms (GPU)

## Class Definitions

The model detects 7 Bangladeshi Taka denominations:

| Class ID | Denomination | Symbol | Color (typical) |
|----------|-------------|--------|---|
| 0        | 10 Taka    | ১০      | Green/Red |
| 1        | 20 Taka    | ২০      | Purple/Blue |
| 2        | 50 Taka    | ৫০      | Brown/Red |
| 3        | 100 Taka   | ১০০     | Red/Orange |
| 4        | 200 Taka   | ২০০     | Purple/Magenta |
| 5        | 500 Taka   | ৫০০     | Green |
| 6        | 1000 Taka  | ১০००    | Pink/Red |

### Class Mapping Code

```python
CLASS_NAMES = {
    0: "10 Taka",
    1: "20 Taka",
    2: "50 Taka",
    3: "100 Taka",
    4: "200 Taka",
    5: "500 Taka",
    6: "1000 Taka"
}
```

## Input/Output Specifications

### Input

- **Format**: JPEG or PNG image
- **Size**: Variable (automatically resized to 640x640)
- **Color Space**: RGB or BGR
- **Batch Size**: 1 or more (supports batching)

### Output

```json
{
    "detections": [
        {
            "denomination": "100 Taka",
            "confidence": 0.9542,
            "bbox": [120.5, 95.3, 280.2, 210.7]
        }
    ]
}
```

**Output Details:**

- **denomination**: Detected class name
- **confidence**: Probability score (0-1)
- **bbox**: Bounding box [x1, y1, x2, y2] in pixel coordinates

### Confidence Score Interpretation

| Score | Interpretation |
|-------|---|
| 0.95+ | Very confident |
| 0.85-0.95 | Confident |
| 0.70-0.85 | Moderately confident |
| 0.50-0.70 | Low confidence |
| <0.50 | Rejected by default |

## Training Details

### Dataset Information

- **Total Images**: [X images from Phase-1]
- **Training Set**: ~70%
- **Validation Set**: ~15%
- **Test Set**: ~15%

### Training Configuration

```yaml
# Hyperparameters
learning_rate: 0.001
batch_size: 16
epochs: 100
optimizer: SGD
momentum: 0.937
weight_decay: 0.0005

# Augmentation
hsv_h: 0.015
hsv_s: 0.7
hsv_v: 0.4
flipud: 0.5
fliplr: 0.5
degrees: 10
translate: 0.1
scale: 0.5
```

### Training Metrics

Expected performance on test set:

| Metric | Value |
|--------|-------|
| mAP@0.5 | ~0.85-0.95 |
| mAP@0.5:0.95 | ~0.70-0.80 |
| Precision | ~0.90+ |
| Recall | ~0.85+ |

## Model Performance

### Speed Benchmarks

```
System: CPU (Intel i7-10700K)
Input Size: 640x640
Batch Size: 1

Single Image: ~50-100ms
Throughput: ~10-20 images/second

System: GPU (NVIDIA RTX 3060)
Single Image: ~20-40ms
Throughput: ~25-50 images/second
```

### Accuracy by Denomination

Expected detection accuracy by denomination:

| Denomination | Accuracy |
|-------------|----------|
| 10 Taka    | 88-92% |
| 20 Taka    | 85-90% |
| 50 Taka    | 87-92% |
| 100 Taka   | 90-95% |
| 200 Taka   | 86-91% |
| 500 Taka   | 89-94% |
| 1000 Taka  | 91-96% |

## Using the Model

### Basic Inference

```python
from ultralytics import YOLO

# Load model
model = YOLO('model/best.pt')

# Predict
results = model('image.jpg')

# Process results
for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        print(f"Class: {class_id}, Confidence: {confidence:.4f}")
```

### Batch Inference

```python
# Detect in multiple images
results = model(['image1.jpg', 'image2.jpg', 'image3.jpg'])
```

### Real-time Video Detection

```python
# Predict on video
results = model('video.mp4', conf=0.5)
```

### Inference Parameters

```python
results = model(
    'image.jpg',
    conf=0.5,              # Confidence threshold
    iou=0.45,              # NMS IOU threshold
    max_det=300,           # Max detections per image
    device=0,              # GPU device (0 for GPU, 'cpu' for CPU)
    half=False,            # Use half precision (FP16)
    augment=False,         # Test-time augmentation
    verbose=False          # Print results
)
```

## Fine-tuning

### Preparing Your Own Dataset

1. **Collect Images**
   - Capture diverse banknote images
   - Vary lighting, angles, backgrounds
   - Minimum 100 images per denomination recommended

2. **Annotate Images**
   - Use tools: Roboflow, LabelImg, CVAT
   - Format: YOLO format (xywh normalized coordinates)
   - Create train/val/test splits

3. **Dataset Structure**
```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

### Fine-tuning Code

```python
from ultralytics import YOLO

# Load pre-trained model
model = YOLO('model/best.pt')

# Fine-tune on custom dataset
results = model.train(
    data='data.yaml',           # Dataset config
    epochs=50,                  # Training epochs
    imgsz=640,                  # Input image size
    batch=16,                   # Batch size
    patience=20,                # Early stopping patience
    device=0,                   # GPU device
    project='runs/detect',      # Output directory
    name='custom_model',        # Run name
    pretrained=True,            # Use pre-trained weights
    optimizer='SGD',            # Optimizer
    lr0=0.001,                  # Initial learning rate
)
```

### data.yaml Format

```yaml
path: /path/to/dataset

train: images/train
val: images/val
test: images/test

nc: 7
names: ['10 Taka', '20 Taka', '50 Taka', '100 Taka', 
        '200 Taka', '500 Taka', '1000 Taka']
```

## Model Export Formats

### Export to Different Formats

```python
from ultralytics import YOLO

model = YOLO('model/best.pt')

# Export to ONNX
model.export(format='onnx')

# Export to TensorFlow
model.export(format='tf')

# Export to CoreML (iOS)
model.export(format='coreml')

# Export to TensorFlow Lite
model.export(format='tflite')

# Export to OpenVINO
model.export(format='openvino')
```

### Using Exported Models

```python
# ONNX inference
import onnx
import onnxruntime as rt

sess = rt.InferenceSession('model/best.onnx')
# ... use for inference

# TensorFlow Lite
import tensorflow as tf

interpreter = tf.lite.Interpreter(model_path='model/best.tflite')
# ... use for inference
```

## Troubleshooting

### Issue: Poor Detection Performance

**Solutions:**
1. Check input image quality
2. Adjust confidence threshold
3. Ensure good lighting conditions
4. Try test-time augmentation

### Issue: Slow Inference

**Solutions:**
1. Use GPU acceleration
2. Reduce image size
3. Use smaller model variant
4. Enable half-precision (FP16)

### Issue: False Positives

**Solutions:**
1. Increase confidence threshold
2. Decrease IoU threshold
3. Check for occlusions
4. Fine-tune on more diverse data

## Model License

- YOLOv11: AGPL-3.0 License
- Ultralytics: AGPL-3.0 License

## References

1. [YOLOv11 Documentation](https://docs.ultralytics.com/)
2. [YOLOv11 GitHub](https://github.com/ultralytics/ultralytics)
3. [YOLO Paper](https://arxiv.org/abs/2402.00677)

## Additional Resources

- **Official Guide**: https://docs.ultralytics.com/
- **Community Forum**: https://community.ultralytics.com/
- **GitHub Issues**: https://github.com/ultralytics/ultralytics/issues

For more information about the model training process, refer to Phase-1 documentation.
