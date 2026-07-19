import logging
from ultralytics import YOLO
from app.config import MODEL_PATH, CONFIDENCE_THRESHOLD, IOU_THRESHOLD
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model once (singleton pattern)
try:
    if Path(MODEL_PATH).exists():
        model = YOLO(str(MODEL_PATH))
        logger.info(f"Model loaded successfully from {MODEL_PATH}")
    else:
        logger.warning(f"Model file not found at {MODEL_PATH}")
        model = None
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None


def run_inference(image_path):
    """
    Run YOLO inference on a single image.
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        list: YOLO results object
    """
    if model is None:
        raise RuntimeError("Model not loaded. Please check model path configuration.")
    
    try:
        results = model(
            image_path,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False
        )
        return results
    except Exception as e:
        logger.error(f"Error during inference: {e}")
        raise