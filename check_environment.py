#!/usr/bin/env python
"""
Environment Verification Script
================================

This script verifies that all required dependencies are installed
and the environment is properly configured.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    print(f"\n🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print("✅ Python version is compatible")
    return True


def check_packages():
    """Check if all required packages are installed"""
    print("\n📦 Checking installed packages...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'torch',
        'torchvision',
        'opencv',
        'ultralytics',
        'numpy',
        'PIL',
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required packages are installed")
    return True


def check_model_files():
    """Check if required model files exist"""
    print("\n🤖 Checking model files...")
    
    base_path = Path(__file__).parent
    models = {
        'yolov8n-face.pt': 'Face detection model',
        'repvgg.pth': 'Emotion classification model',
    }
    
    all_exist = True
    
    for model_file, description in models.items():
        path = base_path / model_file
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"  ✅ {model_file} ({size_mb:.1f} MB) - {description}")
        else:
            print(f"  ❌ {model_file} NOT FOUND - {description}")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some model files are missing!")
        print("Download them from:")
        print("  - yolov8n-face.pt from: https://github.com/ultralytics/ultralytics")
        print("  - repvgg.pth from: your-repo")
        return False
    
    print("\n✅ All model files are present")
    return True


def check_app_structure():
    """Check if app structure is correct"""
    print("\n📁 Checking application structure...")
    
    base_path = Path(__file__).parent
    required_dirs = [
        'app',
        'app/core',
        'app/models',
        'app/routers',
        'app/services',
    ]
    
    required_files = [
        'app/main.py',
        'app/core/config.py',
        'app/core/security.py',
        'app/models/live_detection.py',
        'app/routers/live_detection.py',
        'app/services/face_detector.py',
        'app/services/emotion_classifier.py',
        'app/services/detection_service.py',
        'run.py',
    ]
    
    all_ok = True
    
    # Check directories
    for dir_path in required_dirs:
        path = base_path / dir_path
        if path.is_dir():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ NOT FOUND")
            all_ok = False
    
    # Check files
    for file_path in required_files:
        path = base_path / file_path
        if path.is_file():
            size_kb = path.stat().st_size / 1024
            print(f"  ✅ {file_path} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {file_path} NOT FOUND")
            all_ok = False
    
    if all_ok:
        print("\n✅ Application structure is correct")
    else:
        print("\n❌ Application structure has issues")
    
    return all_ok


def check_gpu_support():
    """Check if GPU (CUDA) is available"""
    print("\n🎮 Checking GPU support...")
    
    try:
        import torch
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0)
            print(f"  ✅ GPU available: {device_name}")
            print(f"  ✅ CUDA devices: {device_count}")
            print(f"  ✅ CUDA version: {torch.version.cuda}")
        else:
            print("  ⚠️  GPU not available (CPU mode will be used)")
            print("  This is fine for development, but slower for production")
    except Exception as e:
        print(f"  ❌ Error checking GPU: {str(e)}")
        return False
    
    return True


def test_imports():
    """Test if all main imports work"""
    print("\n🔗 Testing imports...")
    
    try:
        print("  Testing: import fastapi")
        import fastapi
        print("  ✅ FastAPI import OK")
    except Exception as e:
        print(f"  ❌ FastAPI import failed: {str(e)}")
        return False
    
    try:
        print("  Testing: import torch")
        import torch
        print("  ✅ PyTorch import OK")
    except Exception as e:
        print(f"  ❌ PyTorch import failed: {str(e)}")
        return False
    
    try:
        print("  Testing: import cv2")
        import cv2
        print("  ✅ OpenCV import OK")
    except Exception as e:
        print(f"  ❌ OpenCV import failed: {str(e)}")
        return False
    
    try:
        print("  Testing: import ultralytics")
        import ultralytics
        print("  ✅ Ultralytics import OK")
    except Exception as e:
        print(f"  ❌ Ultralytics import failed: {str(e)}")
        return False
    
    print("\n✅ All imports successful")
    return True


def run_all_checks():
    """Run all checks and print summary"""
    
    print("\n" + "="*70)
    print("🔍 Environment Verification Report")
    print("="*70)
    
    checks = [
        ("Python Version", check_python_version),
        ("Package Installation", check_packages),
        ("Model Files", check_model_files),
        ("App Structure", check_app_structure),
        ("GPU Support", check_gpu_support),
        ("Import Tests", test_imports),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n❌ Error during {check_name}: {str(e)}")
            results[check_name] = False
    
    # Print summary
    print("\n" + "="*70)
    print("📊 Summary")
    print("="*70 + "\n")
    
    all_passed = True
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*70)
    
    if all_passed:
        print("✅ All checks passed! Your environment is ready.")
        print("\n🚀 Next steps:")
        print("  1. python run.py")
        print("  2. Visit http://127.0.0.1:8000/docs")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 Tips:")
        print("  - Run: pip install -r requirements.txt")
        print("  - Ensure Python 3.8+ is installed")
        print("  - Check model files are in the project root")
    
    print("\n" + "="*70 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
