"""
Comprehensive API Testing Script
Tests all endpoints and validates responses
"""

import requests
import json
import sys
import time
from pathlib import Path

# API Base URL
BASE_URL = "http://localhost:8000"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")


def test_health_check():
    """Test health check endpoint"""
    print_header("Testing Health Check Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            print_success(f"Health check endpoint working")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Connection error: {e}")
        return False


def test_root_endpoint():
    """Test root endpoint"""
    print_header("Testing Root Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Root endpoint working")
            print_info(f"API Version: {data.get('version')}")
            print_info(f"Message: {data.get('message')}")
            return True
        else:
            print_error(f"Root endpoint failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Connection error: {e}")
        return False


def test_single_prediction(image_path):
    """Test single image prediction"""
    print_header(f"Testing Single Image Prediction")
    print_info(f"Image path: {image_path}")
    
    if not Path(image_path).exists():
        print_error(f"Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/predict", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Prediction successful")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Detections found: {data.get('detections_count')}")
            
            if data.get('detections'):
                print_info(f"Detections:")
                for i, det in enumerate(data['detections'], 1):
                    print(f"  {i}. {det['denomination']} - Confidence: {det['confidence']:.4f}")
                    print(f"     BBox: {det['bbox']}")
            
            return True
        else:
            print_error(f"Prediction failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error during prediction: {e}")
        return False


def test_batch_prediction(image_paths):
    """Test batch prediction with multiple images"""
    print_header(f"Testing Batch Prediction")
    print_info(f"Number of images: {len(image_paths)}")
    
    missing_files = [p for p in image_paths if not Path(p).exists()]
    if missing_files:
        print_error(f"Missing files: {missing_files}")
        return False
    
    try:
        files = []
        for image_path in image_paths:
            files.append(('files', open(image_path, 'rb')))
        
        response = requests.post(f"{BASE_URL}/predict-batch", files=files)
        
        # Close all files
        for _, file_obj in files:
            file_obj.close()
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Batch prediction successful")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Total files: {data.get('total_files')}")
            
            results = data.get('results', [])
            for i, result in enumerate(results, 1):
                status = Colors.GREEN + "✓" + Colors.END if result['status'] == 'success' else Colors.RED + "✗" + Colors.END
                print(f"  {status} {result['file_name']} - {result['status']}")
                if result['status'] == 'success':
                    print(f"    Detections: {result.get('detections_count')}")
                else:
                    print(f"    Error: {result.get('error')}")
            
            return True
        else:
            print_error(f"Batch prediction failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error during batch prediction: {e}")
        return False


def test_invalid_file():
    """Test with invalid file"""
    print_header("Testing Error Handling - Invalid File")
    
    try:
        # Create a fake text file
        test_file = Path("test_file.txt")
        test_file.write_text("This is not an image")
        
        with open(test_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/predict", files=files)
        
        test_file.unlink()  # Delete test file
        
        if response.status_code == 400:
            print_success(f"Invalid file correctly rejected with status {response.status_code}")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Expected 400 status, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error during test: {e}")
        return False


def test_no_file():
    """Test with no file"""
    print_header("Testing Error Handling - No File")
    
    try:
        response = requests.post(f"{BASE_URL}/predict")
        
        if response.status_code >= 400:
            print_success(f"No file correctly rejected with status {response.status_code}")
            return True
        else:
            print_error(f"Expected error status, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error during test: {e}")
        return False


def create_sample_image():
    """Create a sample image for testing"""
    try:
        from PIL import Image
        import numpy as np
        
        # Create a simple colored image
        img_array = np.random.randint(0, 256, (640, 640, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        
        sample_path = "sample_test_image.jpg"
        img.save(sample_path)
        print_info(f"Created sample image: {sample_path}")
        return sample_path
        
    except Exception as e:
        print_error(f"Could not create sample image: {e}")
        return None


def run_all_tests():
    """Run all tests"""
    print_header("BANGLADESHI TAKA DETECTION API - TEST SUITE")
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test 1: Health Check
    results['health_check'] = test_health_check()
    
    # Test 2: Root Endpoint
    results['root_endpoint'] = test_root_endpoint()
    
    # Test 3: Create and test with sample image
    print("\n")
    sample_image = create_sample_image()
    if sample_image:
        results['single_prediction'] = test_single_prediction(sample_image)
        results['batch_prediction'] = test_batch_prediction([sample_image])
        
        # Clean up
        Path(sample_image).unlink()
    
    # Test 4: Error handling
    results['invalid_file'] = test_invalid_file()
    results['no_file'] = test_no_file()
    
    # Print summary
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    failed_tests = total_tests - passed_tests
    
    for test_name, result in results.items():
        status = Colors.GREEN + "PASSED" + Colors.END if result else Colors.RED + "FAILED" + Colors.END
        print(f"  {test_name:30s} : {status}")
    
    print(f"\n{Colors.BOLD}Total Tests: {total_tests}")
    print(f"Passed: {Colors.GREEN}{passed_tests}{Colors.END}")
    print(f"Failed: {Colors.RED}{failed_tests}{Colors.END}{Colors.END}")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"\nSuccess Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.END}")
    
    return passed_tests, failed_tests


if __name__ == "__main__":
    try:
        passed, failed = run_all_tests()
        sys.exit(0 if failed == 0 else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)
