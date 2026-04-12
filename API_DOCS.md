# API Documentation

## Overview

The Face & Emotion Detection API provides endpoints for detecting faces in images and classifying their emotions using deep learning models.

## Base URL

```
http://127.0.0.1:8000
```

## Authentication

Currently, the API does not require authentication by default. To enable API key authentication, set `REQUIRE_API_KEY=True` in `.env` and include the header:

```
X-API-Key: mysecretkey
```

## Endpoints

### 1. Root Endpoint

```
GET /
```

Check if the API is running.

**Response (200 OK):**
```json
{
  "message": "Face & Emotion Detection API",
  "version": "2.0.0",
  "status": "running"
}
```

---

### 2. Health Check

```
GET /health
```

Check the status of all components.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "face_detector": "ready",
  "emotion_classifier": "ready"
}
```

**Possible Values:**
- `status`: "healthy" | "degraded" | "unhealthy"
- `face_detector`: "ready" | "not initialized" | "error"
- `emotion_classifier`: "ready" | "not initialized" | "error"

---

### 3. Detect Faces in Image File

```
POST /detect/image
```

Upload an image file and get face detection with emotion classification.

**Request:**
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `file` (required): Image file (JPG, PNG)

**Example with cURL:**
```bash
curl -X POST \
  -F "file=@photo.jpg" \
  http://127.0.0.1:8000/detect/image
```

**Example with Python:**
```python
import requests

with open('photo.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://127.0.0.1:8000/detect/image',
        files=files
    )
    print(response.json())
```

**Response (200 OK):**
```json
{
  "detections": [
    {
      "bbox": {
        "x1": 150,
        "y1": 100,
        "x2": 350,
        "y2": 450
      },
      "confidence": 0.95,
      "emotion": "happy",
      "emotion_confidence": 0.87
    },
    {
      "bbox": {
        "x1": 400,
        "y1": 120,
        "x2": 600,
        "y2": 480
      },
      "confidence": 0.92,
      "emotion": "neutral",
      "emotion_confidence": 0.78
    }
  ],
  "total_faces": 2
}
```

**Error Responses:**

```
400 Bad Request
```
```json
{
  "detail": "Invalid image file"
}
```

```
503 Service Unavailable
```
```json
{
  "detail": "Models not initialized"
}
```

---

### 4. Detect Faces in Base64 Image

```
POST /detect/base64
```

Send a base64-encoded image string.

**Request:**
- **Content-Type**: application/json
- **Body**:
  ```json
  {
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
  }
  ```

**Example with Python:**
```python
import requests
import base64

with open('photo.jpg', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode()
    response = requests.post(
        'http://127.0.0.1:8000/detect/base64',
        json={'image_base64': image_base64}
    )
    print(response.json())
```

**Response (200 OK):**
```json
{
  "detections": [
    {
      "bbox": {
        "x1": 150,
        "y1": 100,
        "x2": 350,
        "y2": 450
      },
      "confidence": 0.95,
      "emotion": "happy",
      "emotion_confidence": 0.87
    }
  ],
  "total_faces": 1
}
```

---

## Data Models

### Detection Response

```typescript
{
  detections: Detection[],
  total_faces: number
}
```

### Detection Object

```typescript
{
  bbox: BoundingBox,
  confidence: number,      // 0-1, face detection confidence
  emotion: string | null,  // Emotion label or null if no emotion detected
  emotion_confidence: number | null  // 0-1, emotion classification confidence
}
```

### BoundingBox

```typescript
{
  x1: number,  // Top-left x coordinate (pixels)
  y1: number,  // Top-left y coordinate (pixels)
  x2: number,  // Bottom-right x coordinate (pixels)
  y2: number   // Bottom-right y coordinate (pixels)
}
```

---

## Supported Emotions

The emotion classifier supports 8 emotion classes:

1. **stressed** - High stress or anxiety
2. **contempt** - Contempt or disgust
3. **disgust** - Disgust
4. **fear** - Fear or anxiety
5. **happy** - Happiness or joy
6. **neutral** - Neutral expression
7. **sad** - Sadness
8. **surprise** - Surprise or amazement

---

## Configuration

Environment variables can be set in `.env` file:

```bash
# Server
API_HOST=127.0.0.1
API_PORT=8000

# Device (cpu or cuda)
DEVICE=cpu

# Model paths
FACE_MODEL_PATH=yolov8n-face.pt
EMOTION_MODEL_PATH=repvgg.pth

# Thresholds
FACE_CONF_THRESHOLD=0.5
FACE_IOU_THRESHOLD=0.4
EMOTION_TEMPERATURE=1.0

# Limits
MAX_UPLOAD_SIZE=10485760
REQUEST_TIMEOUT=60
```

---

## Performance Notes

- **Face Detection**: Runs on YOLOv8n-face, optimized for speed
- **Emotion Classification**: RepVGG-A0 model, lightweight and fast
- **GPU Support**: Automatically uses CUDA if available
- **Processing Time**: ~100-300ms per image on CPU

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (missing API key) |
| 403 | Forbidden (invalid API key) |
| 500 | Internal Server Error |
| 503 | Service Unavailable (models not initialized) |

---

## Rate Limiting

Currently, there is no rate limiting. In production, consider adding:

- Per-IP rate limiting
- Concurrent request limits
- Per-user quotas

---

## Examples

### Complete Workflow (Python)

```python
import requests
import json
from pathlib import Path

# 1. Check health
response = requests.get('http://127.0.0.1:8000/health')
print("Health:", response.json())

# 2. Detect faces in image
image_path = 'photo.jpg'
if Path(image_path).exists():
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'http://127.0.0.1:8000/detect/image',
            files=files
        )
    
    result = response.json()
    print(f"Found {result['total_faces']} faces:")
    
    for i, det in enumerate(result['detections']):
        print(f"\nFace {i+1}:")
        print(f"  Bbox: ({det['bbox']['x1']}, {det['bbox']['y1']}) to "
              f"({det['bbox']['x2']}, {det['bbox']['y2']})")
        print(f"  Detection confidence: {det['confidence']:.2%}")
        print(f"  Emotion: {det['emotion']} ({det['emotion_confidence']:.2%})")
```

---

## Troubleshooting

### Q: Models not initializing
**A:** Ensure `yolov8n-face.pt` and `repvgg.pth` exist in the project root directory.

### Q: Out of memory errors
**A:** Set `DEVICE=cpu` or reduce image resolution before sending.

### Q: Slow responses
**A:** 
- Ensure GPU is enabled if available
- Check network latency
- Verify image size isn't too large

### Q: No faces detected
**A:**
- Image quality may be poor
- Adjust `FACE_CONF_THRESHOLD` in `.env`
- Ensure faces are clearly visible

---

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
