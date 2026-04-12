# 🎭 Face & Emotion Detection API

A production-ready FastAPI application for real-time face detection and emotion classification using state-of-the-art deep learning models.

## ✨ Features

- **Face Detection**: YOLOv8n-face model for accurate and fast face detection
- **Emotion Classification**: RepVGG model for classifying 8 different emotions
  - stressed, contempt, disgust, fear, happy, neutral, sad, surprise
- **Multiple Input Methods**: Upload images, send base64-encoded images, or use WebSocket
- **REST API**: Well-documented endpoints with automatic Swagger UI
- **CORS Support**: Ready for cross-origin requests
- **Error Handling**: Comprehensive error handling and logging

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
python run.py
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI documentation.

## 📚 API Endpoints

### 1. Health Check

```bash
GET /health
```

Check the status of both models.

**Response:**
```json
{
  "status": "healthy",
  "face_detector": "ready",
  "emotion_classifier": "ready"
}
```

### 2. Detect Faces in Image File

```bash
POST /detect/image
```

Upload an image file and get face detection and emotion classification results.

**Request:**
- File: image/jpeg or image/png

**Response:**
```json
{
  "detections": [
    {
      "bbox": {
        "x1": 100,
        "y1": 100,
        "x2": 300,
        "y2": 400
      },
      "confidence": 0.95,
      "emotion": "happy",
      "emotion_confidence": 0.87
    }
  ],
  "total_faces": 1
}
```

### 3. Detect Faces in Base64 Image

```bash
POST /detect/base64
```

Send a base64-encoded image string.

**Request:**
```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}
```

**Response:**
```json
{
  "detections": [...],
  "total_faces": 0
}
```

## 📊 Response Format

### Detection Object

```json
{
  "bbox": {
    "x1": int,      // Top-left x coordinate
    "y1": int,      // Top-left y coordinate
    "x2": int,      // Bottom-right x coordinate
    "y2": int       // Bottom-right y coordinate
  },
  "confidence": float,           // Face detection confidence (0-1)
  "emotion": string,             // Emotion label
  "emotion_confidence": float    // Emotion classification confidence (0-1)
}
```

## 🔧 Configuration

Edit `app/config.py` to adjust:

- `HOST`: Server host address
- `PORT`: Server port
- Model paths and device (CPU/CUDA)
- Detection thresholds

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app setup
│   ├── models.py               # Pydantic models
│   ├── config.py               # Configuration
│   ├── auth.py                 # Authentication
│   └── services/
│       ├── __init__.py
│       ├── face_detector.py    # YOLOv8 face detection
│       └── emotion_classifier.py # RepVGG emotion classification
├── run.py                      # Entry point
├── Detection.py                # Legacy detection code
├── emotion.py                  # Emotion model utilities
├── repvgg.py                   # RepVGG model architecture
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🧠 Models Used

### YOLOv8n-face
- Lightweight YOLOv8 variant optimized for face detection
- Model file: `yolov8n-face.pt`
- Confidence threshold: 0.5 (adjustable)

### RepVGG-A0
- Efficient RepVGG variant for emotion classification
- 8-class emotion classifier
- Model file: `repvgg.pth`
- Temperature scaling: 1.0 (adjustable)

## 💡 Usage Examples

### Python

```python
import requests
import base64

# Upload image file
with open('photo.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://127.0.0.1:8000/detect/image',
        files=files
    )
    print(response.json())

# Or use base64
with open('photo.jpg', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode()
    response = requests.post(
        'http://127.0.0.1:8000/detect/base64',
        json={'image_base64': image_base64}
    )
    print(response.json())
```

### cURL

```bash
# File upload
curl -X POST \
  -F "file=@photo.jpg" \
  http://127.0.0.1:8000/detect/image

# Base64 (create JSON file first)
curl -X POST \
  -H "Content-Type: application/json" \
  -d @payload.json \
  http://127.0.0.1:8000/detect/base64
```

## 🎯 Performance Tips

1. **GPU Support**: If CUDA is available, the models will automatically use it
2. **Batch Processing**: For multiple images, consider sending them sequentially
3. **Image Size**: Optimal performance with images between 640x480 and 1920x1080
4. **File Format**: JPG and PNG are supported

## ⚙️ Troubleshooting

### Models not initializing
- Ensure `yolov8n-face.pt` and `repvgg.pth` are in the project root
- Check GPU availability if using CUDA

### Out of memory errors
- Use CPU instead of GPU in config
- Reduce image resolution before sending

### Slow inference
- Check if GPU is being used
- Verify model files are on fast storage

## 📝 License

This project is open source.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
