"""
Face Detection Service using YOLOv8
"""

import torch
from ultralytics import YOLO
import logging

logger = logging.getLogger(__name__)


class FaceDetector:
    """Face detection using YOLOv8n-face model"""
    
    def __init__(self, model_path='yolov8n-face.pt', device='cpu', conf_threshold=0.5, iou_threshold=0.4):
        """
        Initialize face detector.
        
        Args:
            model_path: Path to YOLOv8 face model
            device: Device to run inference on ('cpu' or 'cuda')
            conf_threshold: Confidence threshold for detections
            iou_threshold: IoU threshold for NMS
        """
        logger.info("🔥 Initializing Face Detector with YOLOv8n-face")
        
        self.model = YOLO(model_path)
        self.device = device
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        self.model.to(self.device)
        logger.info(f"✅ Face Detector initialized on device: {device}")
    
    def detect_faces(self, image):
        """
        Detect faces in an image.
        
        Args:
            image: Input image (numpy array, BGR format from OpenCV)
            
        Returns:
            List of detections with format:
            [
                {
                    'bbox': [x1, y1, x2, y2],
                    'confidence': float,
                    'class': int
                },
                ...
            ]
        """
        results = self.model(image, conf=self.conf_threshold, iou=self.iou_threshold)
        detections = []
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                cls = box.cls[0].cpu().numpy()
                
                detections.append({
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': float(conf),
                    'class': int(cls)
                })
        
        return detections
    
    def draw_detections(self, image, detections):
        """
        Draw bounding boxes and labels on image.
        
        Args:
            image: Input image
            detections: List of detections with emotion labels
            
        Returns:
            Image with drawn detections
        """
        import cv2
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            label = det.get('emotion', 'Face')
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            cv2.putText(
                image, 
                label, 
                (x1, y1 - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, 
                (0, 255, 255), 
                2
            )
        
        return image
