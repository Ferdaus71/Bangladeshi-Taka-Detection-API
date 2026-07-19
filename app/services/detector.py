import logging
from app.predictor import run_inference
from app.classes import CLASS_NAMES

logger = logging.getLogger(__name__)


def detect_notes(image_path):
    """
    Detect Bangladeshi Taka notes in an image.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        list: List of detections with denomination, confidence, and bounding box
    """
    try:
        results = run_inference(image_path)
        
        detections = []
        
        for result in results:
            if result.boxes is None or len(result.boxes) == 0:
                logger.info(f"No detections found in image")
                continue
            
            for box in result.boxes:
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
                        "bbox": [
                            round(x1, 2),
                            round(y1, 2),
                            round(x2, 2),
                            round(y2, 2)
                        ]
                    }
                    detections.append(detection)
                    logger.debug(f"Detection: {detection}")
                    
                except Exception as e:
                    logger.error(f"Error processing box: {e}")
                    continue
        
        return detections
        
    except Exception as e:
        logger.error(f"Error in detect_notes: {e}")
        raise