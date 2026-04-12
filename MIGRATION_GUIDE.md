# Migration Guide: OpenCV to FastAPI

## Overview

تم تحويل المشروع من تطبيق OpenCV بسيط إلى FastAPI production-ready API.

## التغييرات الرئيسية

### قبل: كود OpenCV مباشر

```python
# Detection.py - تطبيق OpenCV بسيط
cam = cv2.VideoCapture(0)
detector = FaceDetector()

while True:
    ret, frame = cam.read()
    detections = detector.detect_faces(frame)
    # ... معالجة يدوية
```

### الآن: FastAPI API

```python
# app/main.py - تطبيق FastAPI
@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    # معالجة آلية وموثقة
    frame = cv2.imdecode(...)
    detections = face_detector.detect_faces(frame)
    return FaceDetectionResponse(...)
```

## هيكل المشروع

### قبل
```
project/
├── Detection.py        # كود رئيسي
├── emotion.py          # فئات العواطف
├── repvgg.py          # البنية المعمارية
├── run.py             # تشغيل بسيط
└── requirements.txt
```

### الآن
```
project/
├── run.py                         # Entry point
├── requirements.txt               # Dependencies
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app
│   ├── models.py                 # Pydantic models
│   ├── config.py                 # Configuration
│   ├── auth.py                   # Authentication
│   └── services/
│       ├── __init__.py
│       ├── face_detector.py      # Face detection service
│       └── emotion_classifier.py # Emotion classification service
├── test_api.py                   # Integration tests
├── README.md                     # Documentation
├── API_DOCS.md                   # Detailed API docs
├── Dockerfile                    # Docker support
├── docker-compose.yml            # Docker Compose
├── .gitignore
├── .env.example
└── requirements-dev.txt          # Dev dependencies
```

## الفوائد الرئيسية

### 1. API HTTP المعياري
```bash
# قبل: تطبيق OpenCV محلي فقط
# الآن: يمكن استدعاء الـ API من أي مكان

curl -X POST -F "file=@image.jpg" http://127.0.0.1:8000/detect/image
```

### 2. التوثيق التلقائي
```
# Swagger UI: http://127.0.0.1:8000/docs
# ReDoc: http://127.0.0.1:8000/redoc
```

### 3. معايير الصناعة
- Pydantic models للتحقق من المدخلات
- CORS support
- Error handling موحد
- Logging منظم

### 4. سهولة التوسع
```python
# إضافة endpoint جديد سهل جداً
@app.post("/detect/video")
async def detect_video(file: UploadFile):
    # implementation
    pass
```

### 5. Docker support
```bash
docker-compose up
```

## كيفية الاستخدام

### بدء التطبيق

```bash
# تثبيت المكتبات
pip install -r requirements.txt

# تشغيل الخادم
python run.py

# زيارة الـ API
# - API: http://127.0.0.1:8000
# - Docs: http://127.0.0.1:8000/docs
```

### استدعاء الـ API

#### Python
```python
import requests

# Upload image
with open('photo.jpg', 'rb') as f:
    response = requests.post(
        'http://127.0.0.1:8000/detect/image',
        files={'file': f}
    )
    print(response.json())
```

#### cURL
```bash
curl -X POST \
  -F "file=@photo.jpg" \
  http://127.0.0.1:8000/detect/image
```

#### JavaScript
```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://127.0.0.1:8000/detect/image', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log(result);
```

## المقارنة: قبل وبعد

| الميزة | قبل | بعد |
|--------|------|-----|
| نوع التطبيق | OpenCV Script | FastAPI Server |
| الواجهة | CLI | HTTP REST API |
| التوثيق | لا توجد | Swagger + ReDoc + Markdown |
| الإدخال | Webcam فقط | Files, Base64, WebSocket |
| الخطأ | Print statements | Structured JSON errors |
| التصحيح | Logging يدوي | Structured logging |
| الاختبار | يدوي | Automated + Integration tests |
| الإنتشار | محلي فقط | Docker, Cloud-ready |
| الأداء | Single-threaded | Async/Concurrent |
| المراقبة | لا توجد | Health checks, Metrics |

## ملفات الخدمات الأصلية

الملفات الأصلية محفوظة كمرجع:

- `Detection.py` - الكود الأصلي للكشف عن الوجوه
- `emotion.py` - الكود الأصلي لتصنيف العواطف
- `repvgg.py` - بنية نموذج RepVGG
- `dd.py` - ملف اختبار تحميل النموذج

يمكن الرجوع إليها للمرجعية أو دمج أجزاء منها.

## متطلبات الهجرة الكاملة

إذا كنت تريد دمج كل شيء بالكامل:

1. ✅ FastAPI app setup
2. ✅ Service classes for detection
3. ✅ Pydantic models
4. ✅ API endpoints
5. ⏳ WebSocket for real-time streaming (optional)
6. ⏳ Database integration (optional)
7. ⏳ Authentication/Authorization (optional)
8. ⏳ Rate limiting (optional)

## الخطوات التالية

### للتطوير

```bash
# تثبيت مكتبات التطوير
pip install -r requirements-dev.txt

# تشغيل الاختبارات
pytest test_api.py

# التحقق من الجودة
black app/
flake8 app/
mypy app/
```

### للإنتاج

```bash
# استخدام Docker
docker build -t emotion-detection .
docker run -p 8000:8000 emotion-detection

# أو مع Docker Compose
docker-compose up -d
```

### للاندماج

```bash
# مع تطبيق ويب (React, Vue, etc.)
# استخدم endpoint: POST /detect/image أو /detect/base64

# مع تطبيق موبايل
# استخدم نفس الـ HTTP endpoints

# مع تطبيق سطح المكتب
# استخدم requests library في Python
```

## الأسئلة الشائعة

**Q: هل يزال بإمكاني استخدام كود OpenCV الأصلي؟**
A: نعم، الملفات الأصلية محفوظة. لكن الكود الجديد أفضل وأكثر مرونة.

**Q: هل يتطلب تغيير نماذج ML؟**
A: لا، نفس نماذج YOLO و RepVGG المستخدمة.

**Q: هل يمكن استخدام GPU؟**
A: نعم، عيّن `DEVICE=cuda` في `.env`

**Q: كيف يمكن إضافة معالجة الفيديو المباشرة؟**
A: استخدم WebSocket endpoint (انظر WEBSOCKET_EXAMPLE.md)

## دعم إضافي

للمزيد من المعلومات، اطلع على:
- `README.md` - نظرة عامة سريعة
- `API_DOCS.md` - توثيق الـ API التفصيلي
- `WEBSOCKET_EXAMPLE.md` - مثال WebSocket المتقدم
- `app/main.py` - كود التطبيق الرئيسي
