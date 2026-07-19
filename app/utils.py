import shutil
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_uploaded_file(upload_file, destination):
    """
    Save an uploaded file to the destination path.
    
    Args:
        upload_file: FastAPI UploadFile object
        destination: Destination file path
        
    Raises:
        IOError: If file cannot be saved
    """
    try:
        # Ensure destination directory exists
        dest_dir = os.path.dirname(destination)
        os.makedirs(dest_dir, exist_ok=True)
        
        # Save file
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        logger.info(f"File saved successfully to {destination}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving file to {destination}: {e}")
        raise IOError(f"Failed to save file: {e}")


def get_file_size(file_path):
    """
    Get file size in MB
    
    Args:
        file_path: Path to file
        
    Returns:
        float: File size in MB
    """
    try:
        return os.path.getsize(file_path) / (1024 * 1024)
    except Exception as e:
        logger.error(f"Error getting file size: {e}")
        return 0


def delete_file(file_path):
    """
    Delete a file safely
    
    Args:
        file_path: Path to file to delete
        
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {e}")
        return False