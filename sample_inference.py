"""
Sample Inference Script
Demonstrates how to perform inference using the trained YOLOv11 model
"""

import sys
from pathlib import Path
import logging

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.predictor import run_inference
from app.classes import CLASS_NAMES
from app.config import MODEL_PATH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_separator(title=""):
    """Print a formatted separator"""
    width = 70
    if title:
        print(f"\n{'='*width}")
        print(f"{title.center(width)}")
        print(f"{'='*width}\n")
    else:
        print(f"\n{'='*width}\n")


def print_detection(detection_index, detection):
    """Print formatted detection information"""
    print(f"\nDetection {detection_index}:")
    print(f"  Denomination: {detection['denomination']}")
    print(f"  Confidence: {detection['confidence']:.2%}")
    print(f"  Bounding Box: ({detection['bbox'][0]:.1f}, {detection['bbox'][1]:.1f}) -> "
          f"({detection['bbox'][2]:.1f}, {detection['bbox'][3]:.1f})")


def run_single_inference(image_path):
    """
    Run inference on a single image
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        list: List of detections
    """
    print_separator("SINGLE IMAGE INFERENCE")
    
    image_path = Path(image_path)
    
    if not image_path.exists():
        logger.error(f"Image file not found: {image_path}")
        return []
    
    logger.info(f"Processing image: {image_path}")
    print(f"Image: {image_path.name}")
    print(f"File size: {image_path.stat().st_size / 1024:.2f} KB")
    
    try:
        # Run inference
        results = run_inference(str(image_path))
        
        # Process results
        detections = []
        for result in results:
            if result.boxes is None or len(result.boxes) == 0:
                logger.info("No banknotes detected in image")
                print("\nResult: No banknotes detected")
                return []
            
            print(f"\nDetections found: {len(result.boxes)}")
            
            for i, box in enumerate(result.boxes, 1):
                try:
                    class_id = int(box.cls[0].item()) if hasattr(box.cls[0], 'item') else int(box.cls[0])
                    confidence = float(box.conf[0].item()) if hasattr(box.conf[0], 'item') else float(box.conf[0])
                    
                    # Get bounding box coordinates
                    bbox_coords = box.xyxy[0]
                    if hasattr(bbox_coords, 'tolist'):
                        x1, y1, x2, y2 = bbox_coords.tolist()
                    else:
                        x1, y1, x2, y2 = [float(c) for c in bbox_coords]
                    
                    detection = {
                        "denomination": CLASS_NAMES.get(class_id, f"Unknown_{class_id}"),
                        "confidence": round(confidence, 4),
                        "bbox": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)]
                    }
                    detections.append(detection)
                    print_detection(i, detection)
                    
                except Exception as e:
                    logger.error(f"Error processing detection: {e}")
                    continue
        
        return detections
        
    except Exception as e:
        logger.error(f"Error during inference: {e}", exc_info=True)
        return []


def run_batch_inference(image_paths):
    """
    Run inference on multiple images
    
    Args:
        image_paths (list): List of image file paths
        
    Returns:
        dict: Results for all images
    """
    print_separator("BATCH INFERENCE")
    
    all_results = {}
    
    for idx, image_path in enumerate(image_paths, 1):
        print(f"\n[{idx}/{len(image_paths)}] Processing: {Path(image_path).name}")
        detections = run_single_inference(image_path)
        all_results[image_path] = detections
    
    return all_results


def analyze_detections(detections):
    """
    Analyze detection results
    
    Args:
        detections (list): List of detections
    """
    print_separator("DETECTION ANALYSIS")
    
    if not detections:
        print("No detections found")
        return
    
    # Total detections
    print(f"Total detections: {len(detections)}")
    
    # Detections by denomination
    denomination_count = {}
    for det in detections:
        denom = det['denomination']
        denomination_count[denom] = denomination_count.get(denom, 0) + 1
    
    print("\nDetections by denomination:")
    for denom, count in sorted(denomination_count.items()):
        print(f"  {denom}: {count}")
    
    # Confidence statistics
    confidences = [det['confidence'] for det in detections]
    print(f"\nConfidence statistics:")
    print(f"  Average: {sum(confidences) / len(confidences):.4f}")
    print(f"  Min: {min(confidences):.4f}")
    print(f"  Max: {max(confidences):.4f}")
    
    # Detections with high confidence
    high_conf = [d for d in detections if d['confidence'] > 0.8]
    print(f"\nHigh confidence detections (>0.8): {len(high_conf)}")


def export_results_json(detections, output_file="results.json"):
    """
    Export results to JSON file
    
    Args:
        detections (list): List of detections
        output_file (str): Output file path
    """
    import json
    
    with open(output_file, 'w') as f:
        json.dump({
            "detections_count": len(detections),
            "detections": detections
        }, f, indent=2)
    
    logger.info(f"Results exported to {output_file}")


def create_sample_image():
    """
    Create a sample image for testing if no image is available
    
    Returns:
        str: Path to the sample image
    """
    try:
        from PIL import Image, ImageDraw
        import numpy as np
        
        # Create a colored image with text
        img = Image.new('RGB', (640, 480), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add some shapes and text
        draw.rectangle([100, 100, 300, 250], outline='blue', width=2)
        draw.text((200, 200), "Sample Image", fill='black')
        
        sample_path = "sample_image.jpg"
        img.save(sample_path)
        
        logger.info(f"Sample image created: {sample_path}")
        return sample_path
        
    except Exception as e:
        logger.error(f"Could not create sample image: {e}")
        return None


def main():
    """
    Main function - demonstration of inference pipeline
    """
    print_separator("BANGLADESHI TAKA DETECTION - INFERENCE DEMO")
    
    # Check if model exists
    print(f"Model path: {MODEL_PATH}")
    if not Path(MODEL_PATH).exists():
        logger.error(f"Model not found at {MODEL_PATH}")
        logger.info("Please download the trained model weights and place them in the model/ directory")
        return
    
    logger.info("Model loaded successfully")
    
    # Example 1: Single image inference
    print("\n" + "="*70)
    print("EXAMPLE 1: Single Image Inference".center(70))
    print("="*70)
    
    # Check if sample images exist
    sample_images = list(Path("sample_images").glob("*.jpg")) if Path("sample_images").exists() else []
    
    if sample_images:
        print(f"\nFound {len(sample_images)} sample images")
        image_path = str(sample_images[0])
        detections = run_single_inference(image_path)
        analyze_detections(detections)
    else:
        logger.info("No sample images found in sample_images/ directory")
        print("\nTo test inference, place your test images in 'sample_images/' directory")
        print("Supported formats: .jpg, .png")
    
    # Example 2: Display class information
    print_separator("CLASS INFORMATION")
    print(f"Total classes: {len(CLASS_NAMES)}")
    print("\nClasses:")
    for class_id, class_name in CLASS_NAMES.items():
        print(f"  Class {class_id}: {class_name}")
    
    # Example 3: Configuration information
    print_separator("CONFIGURATION")
    from app.config import CONFIDENCE_THRESHOLD, IOU_THRESHOLD
    print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}")
    print(f"IOU Threshold: {IOU_THRESHOLD}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInference interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
