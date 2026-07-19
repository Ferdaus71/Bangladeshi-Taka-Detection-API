from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model path
MODEL_PATH = BASE_DIR / "model" / "best.pt"

# Upload folder
UPLOAD_DIR = BASE_DIR / "uploads"

# Output folder
OUTPUT_DIR = BASE_DIR / "outputs"

# API Information
API_TITLE = "Bangladeshi Taka Note Detection API"
API_VERSION = "1.0.0"

# Model configuration
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# Allowed file extensions
ALLOWED_EXTENSIONS = ["jpeg", "jpg", "png"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB