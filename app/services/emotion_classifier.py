"""
Emotion Classification Service using RepVGG
"""

import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import cv2
import logging
from PIL import Image

logger = logging.getLogger(__name__)


class EmotionClassifier:
    """Emotion classification using RepVGG model"""
    
    # 8 emotions supported by the model
    EMOTIONS = ("stressed", "contempt", "disgust", "fear", "happy", "neutral", "sad", "surprise")
    
    def __init__(self, device='cpu', model_path='repvgg.pth', temperature=1.0):
        """
        Initialize emotion classifier.
        
        Args:
            device: Device to run inference on ('cpu' or 'cuda')
            model_path: Path to RepVGG model weights
            temperature: Temperature for softmax scaling (>1.0 softens predictions)
        """
        logger.info("🔥 Initializing Emotion Classifier with RepVGG")
        
        try:
            from repvgg import create_RepVGG_A0
            self.device = device
            self.temperature = temperature
            
            # Create model
            self.model = create_RepVGG_A0(deploy=True)
            self.model.to(device)
            
            # Load weights
            state = torch.load(model_path, map_location=device)
            if isinstance(state, dict) and 'state_dict' in state:
                state = state['state_dict']
            self.model.load_state_dict(state)
            
            # Set to eval mode
            torch.backends.cudnn.benchmark = True
            self.model.eval()
            
            logger.info(f"✅ Emotion Classifier initialized on device: {device}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize emotion classifier: {str(e)}")
            raise
    
    def classify_emotions(self, images, return_probs=False):
        """
        Classify emotions in a list of face images.
        
        Args:
            images: List of image arrays (BGR from OpenCV or RGB from PIL)
            return_probs: Whether to return probability distribution
            
        Returns:
            List of results with format:
            [
                {
                    'label': str,
                    'emotion_idx': int,
                    'confidence': float,
                    'probabilities': [float, ...] (optional)
                },
                ...
            ]
        """
        if len(images) == 0:
            return []
        
        with torch.no_grad():
            # Preprocessing pipeline
            normalize = transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
            
            preprocess = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                normalize,
            ])
            
            tensors = []
            for image in images:
                try:
                    if image is None or image.size == 0:
                        # Create dummy black image if invalid
                        pil_image = Image.new('RGB', (224, 224))
                    else:
                        # Handle grayscale
                        if image.ndim == 2:
                            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                        
                        # Convert BGR to RGB
                        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        pil_image = Image.fromarray(rgb)
                except Exception as e:
                    logger.warning(f"Error processing image: {str(e)}, using black image")
                    pil_image = Image.new('RGB', (224, 224))
                
                tensors.append(preprocess(pil_image))
            
            # Stack and inference
            x = torch.stack(tensors)
            outputs = self.model(x.to(self.device))
            
            # Check if outputs are probabilities or logits
            probs_mask = (outputs >= 0).all() and torch.allclose(
                outputs.sum(dim=1), 
                torch.ones(outputs.size(0), device=outputs.device), 
                atol=1e-3
            )
            
            if probs_mask:
                logits = torch.log(outputs.clamp(min=1e-12))
            else:
                logits = outputs
            
            # Apply temperature scaling
            if self.temperature != 1.0:
                probs = F.softmax(logits / float(self.temperature), dim=1)
            else:
                probs = F.softmax(logits, dim=1)
            
            # Format results
            results = []
            for i in range(probs.size(0)):
                top_idx = int(torch.argmax(probs[i]).item())
                top_prob = float(probs[i][top_idx].item())
                label = self.EMOTIONS[top_idx]
                
                result = {
                    'label': label,
                    'emotion_idx': top_idx,
                    'confidence': top_prob
                }
                
                if return_probs:
                    result['probabilities'] = [float(p) for p in probs[i].cpu().numpy()]
                
                results.append(result)
            
            return results
