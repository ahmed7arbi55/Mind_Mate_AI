# 🎭 دليل استخدام API كشف الوجوه والعواطف بـ FastAPI

## 👋 مرحباً بك!

تم تحويل مشروعك من OpenCV البسيط إلى **FastAPI** production-ready.

---

## 🚀 ابدأ الآن في 3 خطوات

### 1️⃣ تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 2️⃣ تشغيل الخادم
```bash
python run.py
```

### 3️⃣ جرب الـ API
افتح في المتصفح: **http://127.0.0.1:8000/docs**

---

## 📖 الملفات الهامة

| الملف | الوصف |
|------|--------|
| `START_HERE.md` | ملخص سريع |
| `README.md` | شرح شامل |
| `API_DOCS.md` | توثيق الـ API |
| `EXAMPLES.py` | أمثلة عملية |
| `MIGRATION_GUIDE.md` | شرح التحويل من OpenCV |

---

## 🎯 الـ API Endpoints

### 1. الفحص السريع
```bash
curl http://127.0.0.1:8000/health
```

### 2. تحميل صورة
```bash
curl -X POST -F "file=@photo.jpg" http://127.0.0.1:8000/detect/image
```

### 3. صورة Base64
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"image_base64":"..."}' \
  http://127.0.0.1:8000/detect/base64
```

---

## 💻 مثال Python

```python
import requests

# اختبر كشف الوجوه
with open('photo.jpg', 'rb') as f:
    response = requests.post(
        'http://127.0.0.1:8000/detect/image',
        files={'file': f}
    )

result = response.json()
print(f"وجوه مكتشفة: {result['total_faces']}")

for i, face in enumerate(result['detections']):
    print(f"الوجه {i+1}: {face['emotion']} ({face['emotion_confidence']:.1%})")
```

---

## 🎓 8 العواطف المدعومة

1. **stressed** - القلق والإجهاد
2. **contempt** - الاحتقار
3. **disgust** - الاشمئزاز
4. **fear** - الخوف
5. **happy** - السعادة
6. **neutral** - محايد
7. **sad** - الحزن
8. **surprise** - المفاجأة

---

## ⚙️ التكوين

عدّل ملف `.env`:

```env
# الخادم
API_HOST=127.0.0.1
API_PORT=8000

# الجهاز (cpu أو cuda)
DEVICE=cpu

# حدود الكشف
FACE_CONF_THRESHOLD=0.5
EMOTION_TEMPERATURE=1.0
```

---

## 🐳 استخدام Docker

```bash
# تشغيل مع Docker Compose
docker-compose up

# أو البناء اليدوي
docker build -t emotion-detection .
docker run -p 8000:8000 emotion-detection
```

---

## ✅ التحقق من البيئة

```bash
python check_environment.py
```

يتحقق من:
- إصدار Python
- المكتبات المثبتة
- ملفات النموذج
- هيكل التطبيق
- دعم GPU

---

## 🧪 اختبار الـ API

```bash
python test_api.py
```

---

## ❓ الأسئلة الشائعة

**س: الخادم لا ينطلق؟**
ج: تأكد من تثبيت المكتبات: `pip install -r requirements.txt`

**س: لا يمكن العثور على النموذج؟**
ج: تأكد من وجود `yolov8n-face.pt` و `repvgg.pth` في جذر المشروع

**س: الأداء بطيء؟**
ج: استخدم GPU إذا كان متاحاً: `DEVICE=cuda`

**س: كيفية دمج WebSocket؟**
ج: راجع `WEBSOCKET_EXAMPLE.md`

---

## 📚 موارد إضافية

```
START_HERE.md          ← ملخص سريع جداً
README.md              ← شرح شامل
API_DOCS.md            ← توثيق API
EXAMPLES.py            ← أمثلة عملية
MIGRATION_GUIDE.md     ← شرح الانتقال
WEBSOCKET_EXAMPLE.md   ← البث المباشر
INDEX.md               ← دليل الملفات
```

---

## 🚀 الخطوة التالية

```bash
python run.py
```

ثم:
- 🌐 API: http://127.0.0.1:8000
- 📖 Docs: http://127.0.0.1:8000/docs
- 📘 ReDoc: http://127.0.0.1:8000/redoc

---

## 💡 نصائح

1. استخدم `/docs` لاختبار الـ API بشكل تفاعلي
2. استخدم `RELOAD=True` في التطوير
3. استخدم Docker للإنتاج
4. راجع `EXAMPLES.py` للأمثلة المختلفة

---

**تم! الآن أنت جاهز للبدء! 🎉**

قم بتشغيل:
```bash
python run.py
```

ثم افتح: http://127.0.0.1:8000/docs
