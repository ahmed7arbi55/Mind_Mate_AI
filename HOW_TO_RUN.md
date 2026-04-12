# 🚀 كيفية تشغيل المشروع

## الطريقة الأولى: التشغيل المباشر (الأسهل)

### على Windows:

#### الخطوة 1: فتح Command Prompt
```
اضغط: Win + R
اكتب: cmd
اضغط: Enter
```

#### الخطوة 2: انتقل إلى مجلد المشروع
```bash
cd C:\Users\ahmed\Downloads\drive-download-20260324T200917Z-1-001
```

#### الخطوة 3: تثبيت المكتبات (إذا لم تثبت بعد)
```bash
pip install -r requirements.txt
```

#### الخطوة 4: تشغيل الخادم
```bash
python run.py
```

**أو** (باستخدام ملف batch):
```bash
run.bat
```

**أو** (باستخدام script بسيط مع فحوصات):
```bash
python start_server.py
```

---

## الطريقة الثانية: استخدام Python IDE

### VS Code:

1. افتح المشروع في VS Code
2. افتح Terminal: `Ctrl + `` (backtick)
3. اكتب: `python run.py`
4. اضغط Enter

### PyCharm:

1. افتح المشروع
2. انقر على `run.py`
3. اضغط كليك يميين → Run 'run.py'

---

## الطريقة الثالثة: استخدام Docker

### الخطوة 1: تثبيت Docker
من: https://www.docker.com/products/docker-desktop

### الخطوة 2: تشغيل مع Docker Compose
```bash
docker-compose up
```

---

## الطريقة الرابعة: استخدام Script Python بسيط

```bash
python start_server.py
```

يقوم بـ:
1. ✅ فحص Python version
2. ✅ فحص المكتبات
3. ✅ فحص ملفات النموذج
4. ✅ فحص ملفات التطبيق
5. ✅ بدء الخادم

---

## بعد التشغيل

### افتح المتصفح:

```
🌐 الـ API:
   http://127.0.0.1:8000

📖 التوثيق التفاعلي (Swagger):
   http://127.0.0.1:8000/docs

📘 التوثيق البديل (ReDoc):
   http://127.0.0.1:8000/redoc
```

---

## مثال: اختبار الـ API

### في نفس الـ Command Prompt (نافذة جديدة):

#### اختبر Health Check:
```bash
curl http://127.0.0.1:8000/health
```

#### اختبر كشف الوجوه:
```bash
curl -X POST -F "file=@photo.jpg" http://127.0.0.1:8000/detect/image
```

---

## الأخطاء الشائعة وحلولها

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**الحل:**
```bash
pip install -r requirements.txt
```

### ❌ "Address already in use"

**الحل:** المنفذ 8000 مشغول
```bash
# غيّر المنفذ في .env:
API_PORT=8001

# ثم شغّل:
python run.py
```

### ❌ "FileNotFoundError: yolov8n-face.pt not found"

**الحل:** تأكد أن ملفات النماذج موجودة:
- `yolov8n-face.pt`
- `repvgg.pth`

يجب أن تكون في مجلد المشروع الرئيسي.

### ❌ "CUDA out of memory"

**الحل:** استخدم CPU بدلاً من GPU
```bash
# غيّر في .env:
DEVICE=cpu
```

---

## الملفات المهمة للتشغيل

```
run.py              ← تشغيل مباشر
run.bat             ← تشغيل على Windows
start_server.py     ← تشغيل مع فحوصات
docker-compose.yml  ← تشغيل مع Docker
requirements.txt    ← المكتبات المطلوبة
```

---

## المتغيرات الهامة (.env)

```env
# المنفذ
API_PORT=8000

# الجهاز (cpu أو cuda)
DEVICE=cpu

# التطوير (reload تلقائي)
RELOAD=True

# DEBUG mode
DEBUG=True
```

---

## ملاحظات

✅ الخادم سيعيد التحميل تلقائياً عند تعديل الكود (إذا كان `RELOAD=True`)

✅ يمكنك اختبار الـ API من `/docs` مباشرة في المتصفح

✅ للإيقاف: اضغط `Ctrl + C` في Command Prompt

---

## 🎯 الآن أنت جاهز!

اختر الطريقة المناسبة لك وشغّل المشروع! 🚀
