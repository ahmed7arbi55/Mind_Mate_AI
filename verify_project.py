#!/usr/bin/env python
"""
FastAPI Project Verification Script
====================================

This script verifies that all required files have been created correctly
for the FastAPI Face & Emotion Detection API.
"""

import os
from pathlib import Path


def check_files():
    """Check if all required files exist"""
    
    base_path = Path(__file__).parent
    
    required_files = {
        "Core Application": [
            "app/__init__.py",
            "app/main.py",
            "app/models/__init__.py",
            "app/models/live_detection.py",
            "app/core/__init__.py",
            "app/core/config.py",
            "app/core/security.py",
            "app/routers/__init__.py",
            "app/routers/live_detection.py",
            "app/services/__init__.py",
            "app/services/face_detector.py",
            "app/services/emotion_classifier.py",
            "app/services/detection_service.py",
            "app/services/runtime_state.py",
            "app/services/legacy.py",
        ],
        "Entry Points": [
            "run.py",
        ],
        "Configuration": [
            "requirements.txt",
            "requirements-dev.txt",
            ".env.example",
            ".gitignore",
        ],
        "Documentation": [
            "README.md",
            "API_DOCS.md",
            "MIGRATION_GUIDE.md",
            "WEBSOCKET_EXAMPLE.md",
            "CONVERSION_COMPLETE.md",
        ],
        "Testing & Deployment": [
            "test_api.py",
            "Dockerfile",
            "docker-compose.yml",
        ],
        "Legacy Files (Preserved)": [
            "Detection.py",
            "emotion.py",
            "repvgg.py",
            "dd.py",
            "yolov8n-face.pt",
            "repvgg.pth",
        ]
    }
    
    print("\n" + "=" * 70)
    print("🔍 FastAPI Project Structure Verification")
    print("=" * 70 + "\n")
    
    all_good = True
    
    for category, files in required_files.items():
        print(f"\n📁 {category}:")
        print("-" * 70)
        
        for file_path in files:
            full_path = base_path / file_path
            exists = full_path.exists()
            status = "✅" if exists else "❌"
            file_name = Path(file_path).name
            
            print(f"  {status} {file_path:<50}", end="")
            
            if exists and file_path.endswith(('.py', '.md', '.txt')):
                try:
                    size = full_path.stat().st_size
                    if size > 1024:
                        print(f"({size // 1024}KB)")
                    else:
                        print(f"({size}B)")
                except:
                    print()
            else:
                print()
            
            if not exists and "Legacy" not in category:
                all_good = False
    
    print("\n" + "=" * 70)
    
    if all_good:
        print("✅ All required files are present!")
        print("\n🚀 Next Steps:")
        print("-" * 70)
        print("1. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n2. Run the application:")
        print("   python run.py")
        print("\n3. Visit the API documentation:")
        print("   http://127.0.0.1:8000/docs")
        print("\n4. Test the API:")
        print("   python test_api.py")
    else:
        print("⚠️  Some files are missing!")
        print("\nPlease check the conversion process.")
    
    print("\n" + "=" * 70 + "\n")
    
    return all_good


def show_project_stats():
    """Show project statistics"""
    
    base_path = Path(__file__).parent
    
    print("\n📊 Project Statistics:")
    print("-" * 70)
    
    py_files = list(base_path.glob("**/*.py"))
    md_files = list(base_path.glob("**/*.md"))
    
    py_lines = 0
    for py_file in py_files:
        try:
            py_lines += len(py_file.read_text().split('\n'))
        except:
            pass
    
    print(f"Python files: {len(py_files)}")
    print(f"Python lines of code: ~{py_lines:,}")
    print(f"Documentation files: {len(md_files)}")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    success = check_files()
    show_project_stats()
    
    if success:
        print("✨ Your FastAPI project is ready to use! ✨\n")
        exit(0)
    else:
        exit(1)
