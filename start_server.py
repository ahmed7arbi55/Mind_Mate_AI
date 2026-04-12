"""
تعليمات تشغيل المشروع
====================

قم بتنفيذ الخطوات التالية لتشغيل المشروع:
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    """Print beautiful banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║   🎭 Face & Emotion Detection API - FastAPI Server 🎭      ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python():
    """Check Python version"""
    print("📌 الخطوة 1: التحقق من Python...")
    print(f"   Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("   ❌ Python 3.8+ مطلوب!")
        return False
    print("   ✅ Python متوافق")
    return True

def check_dependencies():
    """Check if dependencies are installed"""
    print("\n📌 الخطوة 2: التحقق من المكتبات...")
    
    required = ['fastapi', 'uvicorn', 'torch', 'cv2', 'ultralytics']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - غير مثبت")
            missing.append(package)
    
    if missing:
        print(f"\n   ⚠️  المكتبات المفقودة: {', '.join(missing)}")
        print("   تثبيت المكتبات:")
        print("   pip install -r requirements.txt")
        return False
    
    print("   ✅ جميع المكتبات مثبتة")
    return True

def check_models():
    """Check if model files exist"""
    print("\n📌 الخطوة 3: التحقق من ملفات النماذج...")
    
    base_path = Path(__file__).parent
    models = {
        'yolov8n-face.pt': 'Face Detection Model',
        'repvgg.pth': 'Emotion Classification Model',
    }
    
    all_exist = True
    for model_file, desc in models.items():
        path = base_path / model_file
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"   ✅ {model_file} ({size_mb:.1f}MB) - {desc}")
        else:
            print(f"   ❌ {model_file} - غير موجود")
            all_exist = False
    
    return all_exist

def check_app_files():
    """Check if app files exist"""
    print("\n📌 الخطوة 4: التحقق من ملفات التطبيق...")
    
    base_path = Path(__file__).parent
    files = [
        'app/main.py',
        'app/models/live_detection.py',
        'app/routers/live_detection.py',
        'app/core/config.py',
        'app/core/security.py',
        'app/services/face_detector.py',
        'app/services/emotion_classifier.py',
        'app/services/detection_service.py',
    ]
    
    all_exist = True
    for file_path in files:
        path = base_path / file_path
        if path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - غير موجود")
            all_exist = False
    
    return all_exist

def start_server():
    """Start the FastAPI server"""
    print("\n📌 الخطوة 5: تشغيل الخادم...")
    print("\n" + "="*60)
    print("🚀 بدء تشغيل الخادم...")
    print("="*60)
    print("\n🌐 API متاح على:")
    print("   • API: http://127.0.0.1:8000")
    print("   • Docs: http://127.0.0.1:8000/docs")
    print("   • ReDoc: http://127.0.0.1:8000/redoc")
    print("\n⏹️  للإيقاف: اضغط Ctrl+C")
    print("\n" + "="*60 + "\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✅ تم إيقاف الخادم بنجاح!")
    except Exception as e:
        print(f"\n❌ خطأ: {str(e)}")
        return False
    
    return True

def main():
    """Main entry point"""
    print_banner()
    
    # Run checks
    checks = [
        ("Python Version", check_python),
        ("Dependencies", check_dependencies),
        ("Model Files", check_models),
        ("App Files", check_app_files),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"   ❌ خطأ: {str(e)}")
            results[name] = False
    
    # Print summary
    print("\n" + "="*60)
    print("📊 ملخص الفحص:")
    print("="*60)
    
    all_ok = True
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_ok = False
    
    print("="*60)
    
    if not all_ok:
        print("\n⚠️  بعض الفحوصات فشلت!")
        print("الرجاء إصلاح المشاكل المذكورة أعلاه.")
        return False
    
    print("\n✅ جميع الفحوصات نجحت!")
    
    # Start server
    input("\nاضغط Enter لبدء الخادم...")
    start_server()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
