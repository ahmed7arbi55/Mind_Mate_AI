# استخدم نسخة Slim عشان الحجم يكون صغير
FROM python:3.11-slim

# تحديد فولدر العمل
WORKDIR /app

# تثبيت الأدوات الأساسية للنظام (لو محتاج مكتبات معينة)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات أولاً (عشان الكاش)
COPY requirements.txt .

# السحر هنا: تثبيت PyTorch نسخة الـ CPU فقط عشان توفر 3 جيجا!
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch torchvision

# تثبيت باقي المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تشغيل FastAPI (تأكد إن اسم ملف التشغيل عندك هو main.py)
# Railway بيحتاج الـ Host يكون 0.0.0.0 والـ Port هو اللي بيحدده
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
