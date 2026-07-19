from pydantic import BaseModel, Field
from typing import List, Optional


class Detection(BaseModel):
    """Model for a single detection result"""
    denomination: str = Field(..., description="Denomination of the Bangladeshi Taka note")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score of the detection")
    bbox: List[float] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2]")


class PredictionResponse(BaseModel):
    """Model for prediction API response"""
    status: str = Field("success", description="Status of the prediction")
    file_name: Optional[str] = Field(None, description="Name of the uploaded file")
    detections_count: int = Field(..., description="Number of detections found")
    detections: List[Detection] = Field(default_factory=list, description="List of detected notes")


class BatchPredictionResult(BaseModel):
    """Model for individual result in batch prediction"""
    file_name: str = Field(..., description="Name of the file")
    status: str = Field(..., description="Status of processing")
    detections_count: Optional[int] = Field(None, description="Number of detections")
    detections: Optional[List[Detection]] = Field(None, description="List of detections")
    error: Optional[str] = Field(None, description="Error message if any")


class BatchPredictionResponse(BaseModel):
    """Model for batch prediction API response"""
    status: str = Field("batch_complete", description="Status of batch processing")
    total_files: int = Field(..., description="Total number of files processed")
    results: List[BatchPredictionResult] = Field(..., description="Results for each file")


class HealthCheckResponse(BaseModel):
    """Model for health check response"""
    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")