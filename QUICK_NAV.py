"""
Quick Navigation Guide
======================

هذا الملف يساعدك على الملاحة السريعة في المشروع.
"""

import os
from pathlib import Path

NAVIGATION = {
    "🚀 ابدأ هنا": [
        ("START_HERE.md", "ملخص سريع جداً"),
        ("README.md", "شرح شامل للمشروع"),
        ("README_AR.md", "نسخة عربية من README"),
    ],
    
    "📖 الوثائق": [
        ("API_DOCS.md", "توثيق API تفصيلي"),
        ("MIGRATION_GUIDE.md", "شرح الانتقال من OpenCV"),
        ("INDEX.md", "دليل الملفات"),
        ("EXAMPLES.py", "أمثلة عملية"),
        ("WEBSOCKET_EXAMPLE.md", "أمثلة WebSocket متقدمة"),
    ],
    
    "🔧 التطوير": [
        ("app/main.py", "كود FastAPI الرئيسي"),
        ("app/models.py", "Pydantic models"),
        ("app/services/face_detector.py", "خدمة كشف الوجوه"),
        ("app/services/emotion_classifier.py", "خدمة تصنيف العواطف"),
    ],
    
    "🧪 الاختبار": [
        ("test_api.py", "اختبار الـ API"),
        ("check_environment.py", "التحقق من البيئة"),
        ("verify_project.py", "التحقق من الهيكل"),
    ],
    
    "🐳 النشر": [
        ("Dockerfile", "Docker image"),
        ("docker-compose.yml", "Docker Compose"),
        (".env.example", "متغيرات البيئة"),
        ("requirements.txt", "المكتبات المطلوبة"),
    ],
    
    "📋 ملخصات": [
        ("CONVERSION_COMPLETE.md", "ملخص التحويل"),
        ("FINAL_SUMMARY.md", "الملخص النهائي"),
    ],
}

def print_navigation():
    """Print navigation guide"""
    
    print("\n" + "="*70)
    print("📑 دليل الملاحة السريعة")
    print("="*70)
    
    for category, files in NAVIGATION.items():
        print(f"\n{category}")
        print("-" * 70)
        
        for file_name, description in files:
            # Check if file exists
            file_path = Path(file_name)
            exists = "✅" if file_path.exists() else "❌"
            print(f"  {exists} {file_name:<40} - {description}")
    
    print("\n" + "="*70)
    print("🚀 الخطوات الأولى:")
    print("-" * 70)
    print("1. اقرأ: START_HERE.md")
    print("2. شغّل: python run.py")
    print("3. زر: http://127.0.0.1:8000/docs")
    print("\n" + "="*70 + "\n")


def print_quick_commands():
    """Print quick commands"""
    
    print("\n" + "="*70)
    print("⚡ أوامر سريعة")
    print("="*70 + "\n")
    
    commands = {
        "تثبيت المكتبات": "pip install -r requirements.txt",
        "التحقق من البيئة": "python check_environment.py",
        "تشغيل الخادم": "python run.py",
        "اختبار الـ API": "python test_api.py",
        "التحقق من الهيكل": "python verify_project.py",
        "تشغيل مع Docker": "docker-compose up",
    }
    
    for description, command in commands.items():
        print(f"📌 {description}:")
        print(f"   $ {command}\n")
    
    print("="*70 + "\n")


def print_endpoints():
    """Print available endpoints"""
    
    print("\n" + "="*70)
    print("🔌 الـ Endpoints المتاحة")
    print("="*70 + "\n")
    
    endpoints = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/health", "Health check"),
        ("POST", "/detect/image", "كشف الوجوه من ملف"),
        ("POST", "/detect/base64", "كشف الوجوه من Base64"),
    ]
    
    for method, path, desc in endpoints:
        print(f"  {method:6} {path:<25} - {desc}")
    
    print("\n" + "="*70 + "\n")


def print_file_structure():
    """Print project structure"""
    
    print("\n" + "="*70)
    print("📁 هيكل المشروع")
    print("="*70 + "\n")
    
    structure = """
project/
├── app/
│   ├── main.py              🚀 FastAPI app
│   ├── models.py            📦 Pydantic models
│   ├── config.py            ⚙️  Configuration
│   ├── auth.py              🔐 Authentication
│   └── services/
│       ├── face_detector.py 👁️  Face detection
│       └── emotion_classifier.py 😊 Emotion classification
├── run.py                   ▶️  Start server
├── test_api.py              🧪 Tests
├── Dockerfile               🐳 Docker
├── requirements.txt         📦 Dependencies
├── README.md                📖 Docs
└── [More docs & configs]
"""
    
    print(structure)
    print("="*70 + "\n")


if __name__ == "__main__":
    print_navigation()
    print_quick_commands()
    print_endpoints()
    print_file_structure()
    
    print("\n💡 نصيحة: استخدم START_HERE.md للبدء السريع!")
