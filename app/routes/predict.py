import os
import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.services.detector import detect_notes
from app.utils import save_uploaded_file
from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS

logger = logging.getLogger(__name__)
router = APIRouter()

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/")
async def root():
    """
    Root endpoint to check API status
    """
    return {
        "status": "running",
        "message": "Bangladeshi Taka Note Detection API is running successfully",
        "version": "1.0.0"
    }


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict denomination of Bangladeshi Taka notes in an uploaded image.
    
    Args:
        file: Image file (JPEG or PNG)
        
    Returns:
        JSON: Detected denominations with confidence scores and bounding boxes
    """
    try:
        # Validate file exists and has content
        if not file:
            raise HTTPException(
                status_code=400,
                detail="No file uploaded"
            )
        
        # Validate file type
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Only JPEG and PNG images are allowed."
            )
        
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower().lstrip('.')
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension: .{file_ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        try:
            save_uploaded_file(file, file_path)
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error saving file"
            )
        
        # Run detection
        try:
            detections = detect_notes(file_path)
        except Exception as e:
            logger.error(f"Error during detection: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error during detection process"
            )
        finally:
            # Clean up uploaded file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"Error cleaning up file: {e}")
        
        # Return results
        return {
            "status": "success",
            "file_name": file.filename,
            "detections_count": len(detections),
            "detections": detections
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in predict endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction"
        )


@router.post("/predict-batch")
async def predict_batch(files: list[UploadFile] = File(...)):
    """
    Batch prediction for multiple images.
    
    Args:
        files: List of image files
        
    Returns:
        JSON: Results for all images
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed per request")
    
    results = []
    
    for file in files:
        try:
            # Validate file type
            if file.content_type not in ["image/jpeg", "image/png"]:
                results.append({
                    "file_name": file.filename,
                    "status": "failed",
                    "error": "Invalid file type"
                })
                continue
            
            # Save and process
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            save_uploaded_file(file, file_path)
            
            detections = detect_notes(file_path)
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            
            results.append({
                "file_name": file.filename,
                "status": "success",
                "detections_count": len(detections),
                "detections": detections
            })
            
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {e}")
            results.append({
                "file_name": file.filename,
                "status": "failed",
                "error": str(e)
            })
    
    return {
        "status": "batch_complete",
        "total_files": len(files),
        "results": results
    }