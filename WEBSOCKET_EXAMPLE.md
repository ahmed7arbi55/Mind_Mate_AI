"""
Example: Real-time Camera Feed with FastAPI and WebSockets
===========================================================

This demonstrates how to extend the FastAPI app with WebSocket support
for real-time camera streaming and emotion detection.

To use this, add it to your app/main.py or create a separate app/routes/websocket.py
"""

from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import cv2
import logging
import numpy as np
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class CameraManager:
    """Manages WebSocket connections for camera streaming"""
    
    def __init__(self, face_detector, emotion_classifier):
        self.active_connections: list[WebSocket] = []
        self.face_detector = face_detector
        self.emotion_classifier = emotion_classifier
        self.emotion_stats = defaultdict(int)
        self.start_time = datetime.now()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
    
    async def process_frame(self, frame_data):
        """Process a frame and detect faces/emotions"""
        try:
            # Decode frame
            nparr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return None
            
            # Detect faces
            detections = self.face_detector.detect_faces(frame)
            
            # Classify emotions
            if len(detections) > 0:
                face_crops = []
                for det in detections:
                    x1, y1, x2, y2 = det['bbox']
                    face_crop = frame[y1:y2, x1:x2]
                    face_crops.append(face_crop)
                
                emotion_results = self.emotion_classifier.classify_emotions(face_crops)
                
                for i, det in enumerate(detections):
                    if i < len(emotion_results):
                        det['emotion'] = emotion_results[i]['label']
                        det['emotion_confidence'] = emotion_results[i]['confidence']
                        self.emotion_stats[emotion_results[i]['label']] += 1
            
            return {
                'frame_id': datetime.now().isoformat(),
                'detections': detections,
                'total_faces': len(detections),
                'stats': dict(self.emotion_stats)
            }
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return None


# To add to app/main.py:
"""
from fastapi import WebSocket

# Create camera manager instance (initialize in lifespan)
camera_manager: CameraManager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global face_detector, emotion_classifier, camera_manager
    logger.info("🚀 Initializing...")
    
    face_detector = FaceDetector(model_path='yolov8n-face.pt', device='cpu')
    emotion_classifier = EmotionClassifier(device='cpu')
    camera_manager = CameraManager(face_detector, emotion_classifier)
    
    logger.info("✅ Models initialized")
    yield
    logger.info("🛑 Shutting down")


@app.websocket("/ws/camera")
async def websocket_endpoint(websocket: WebSocket):
    '''
    WebSocket endpoint for real-time camera streaming.
    
    Client should send: base64-encoded frame data
    Server responds with: detection results and statistics
    '''
    await camera_manager.connect(websocket)
    try:
        while True:
            # Receive frame from client
            data = await websocket.receive_bytes()
            
            # Process frame
            result = await camera_manager.process_frame(data)
            
            if result:
                await websocket.send_json(result)
    
    except WebSocketDisconnect:
        camera_manager.disconnect(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        camera_manager.disconnect(websocket)
"""


# JavaScript Client Example:
"""
const ws = new WebSocket('ws://127.0.0.1:8000/ws/camera');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const video = document.getElementById('video');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.onplay = () => {
            const captureFrame = () => {
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                
                // Convert canvas to frame data
                canvas.toBlob(blob => {
                    ws.send(blob);
                }, 'image/jpeg', 0.9);
                
                requestAnimationFrame(captureFrame);
            };
            captureFrame();
        };
    });

ws.onmessage = (event) => {
    const result = JSON.parse(event.data);
    console.log(`Faces detected: ${result.total_faces}`);
    console.log(`Current emotions:`, result.stats);
    
    // Draw detections on canvas
    result.detections.forEach(det => {
        const bbox = det.bbox;
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.strokeRect(
            bbox.x1, bbox.y1,
            bbox.x2 - bbox.x1,
            bbox.y2 - bbox.y1
        );
        
        if (det.emotion) {
            ctx.fillStyle = 'yellow';
            ctx.font = '14px Arial';
            ctx.fillText(
                `${det.emotion} (${(det.emotion_confidence * 100).toFixed(1)}%)`,
                bbox.x1,
                bbox.y1 - 5
            );
        }
    });
};
"""
