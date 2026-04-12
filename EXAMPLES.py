"""
Practical Examples for Face & Emotion Detection API
====================================================

This file contains ready-to-use code examples for different use cases.
"""

# ============================================================================
# Example 1: Simple Image Detection (Python)
# ============================================================================

def example_1_simple_detection():
    """Detect faces in a single image"""
    import requests
    
    # URL of the API
    api_url = "http://127.0.0.1:8000/detect/image"
    
    # Open image file
    with open("photo.jpg", "rb") as f:
        files = {"file": f}
        response = requests.post(api_url, files=files)
    
    # Parse result
    result = response.json()
    print(f"Detected {result['total_faces']} faces:")
    
    for i, detection in enumerate(result['detections']):
        print(f"\nFace {i+1}:")
        print(f"  Position: ({detection['bbox']['x1']}, {detection['bbox']['y1']}) "
              f"to ({detection['bbox']['x2']}, {detection['bbox']['y2']})")
        print(f"  Confidence: {detection['confidence']:.1%}")
        print(f"  Emotion: {detection['emotion']} ({detection['emotion_confidence']:.1%})")


# ============================================================================
# Example 2: Batch Processing Multiple Images (Python)
# ============================================================================

def example_2_batch_processing():
    """Process multiple images"""
    import requests
    from pathlib import Path
    
    api_url = "http://127.0.0.1:8000/detect/image"
    image_folder = Path("./images")
    results = []
    
    for image_file in image_folder.glob("*.jpg"):
        with open(image_file, "rb") as f:
            files = {"file": f}
            response = requests.post(api_url, files=files)
            result = response.json()
            results.append({
                "file": image_file.name,
                "faces": result['total_faces'],
                "detections": result['detections']
            })
        
        print(f"✅ Processed {image_file.name}: {result['total_faces']} faces")
    
    return results


# ============================================================================
# Example 3: Base64 Encoded Image (Python)
# ============================================================================

def example_3_base64_detection():
    """Send base64-encoded image"""
    import requests
    import base64
    
    api_url = "http://127.0.0.1:8000/detect/base64"
    
    # Encode image to base64
    with open("photo.jpg", "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    # Send request
    response = requests.post(
        api_url,
        json={"image_base64": image_base64}
    )
    
    result = response.json()
    print(f"Detected {result['total_faces']} faces")


# ============================================================================
# Example 4: Using with OpenCV (Python)
# ============================================================================

def example_4_opencv_integration():
    """Use the API with OpenCV for image capture"""
    import cv2
    import requests
    import numpy as np
    
    api_url = "http://127.0.0.1:8000/detect/image"
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        
        # Send to API
        files = {'file': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
        response = requests.post(api_url, files=files)
        result = response.json()
        
        # Draw detections on frame
        for detection in result['detections']:
            bbox = detection['bbox']
            emotion = detection['emotion']
            
            # Draw rectangle
            cv2.rectangle(frame, 
                         (bbox['x1'], bbox['y1']),
                         (bbox['x2'], bbox['y2']),
                         (0, 255, 0), 2)
            
            # Draw label
            label = f"{emotion} ({detection['emotion_confidence']:.1%})"
            cv2.putText(frame, label, 
                       (bbox['x1'], bbox['y1'] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (0, 255, 255), 2)
        
        # Show frame
        cv2.imshow('Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


# ============================================================================
# Example 5: Emotion Statistics (Python)
# ============================================================================

def example_5_emotion_statistics():
    """Collect statistics from multiple images"""
    import requests
    from pathlib import Path
    from collections import defaultdict
    
    api_url = "http://127.0.0.1:8000/detect/image"
    emotion_counts = defaultdict(int)
    total_faces = 0
    
    # Process all images
    for image_file in Path("./images").glob("*.jpg"):
        with open(image_file, "rb") as f:
            files = {"file": f}
            response = requests.post(api_url, files=files)
            result = response.json()
            
            total_faces += result['total_faces']
            
            for detection in result['detections']:
                emotion = detection['emotion']
                emotion_counts[emotion] += 1
    
    # Print statistics
    print(f"\n📊 Emotion Statistics:")
    print(f"Total faces detected: {total_faces}")
    print(f"\nBreakdown by emotion:")
    
    for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_faces * 100) if total_faces > 0 else 0
        print(f"  {emotion:12} : {count:3} ({percentage:5.1f}%)")


# ============================================================================
# Example 6: JavaScript Frontend (HTML + JavaScript)
# ============================================================================

HTML_EXAMPLE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face & Emotion Detection</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .upload-area {
            border: 2px dashed #ccc;
            border-radius: 4px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-area:hover {
            border-color: #4CAF50;
            background-color: #f9f9f9;
        }
        input[type="file"] {
            display: none;
        }
        #image-preview {
            max-width: 100%;
            margin-top: 20px;
            display: none;
        }
        .results {
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 4px;
            display: none;
        }
        .result-item {
            padding: 10px;
            background: white;
            margin: 5px 0;
            border-left: 4px solid #4CAF50;
        }
        .loading {
            text-align: center;
            display: none;
        }
        .error {
            color: #d32f2f;
            padding: 10px;
            background-color: #ffebee;
            border-radius: 4px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Face & Emotion Detection</h1>
        
        <div class="upload-area" id="uploadArea">
            <p>Click to upload or drag and drop</p>
            <p style="font-size: 12px; color: #999;">JPG or PNG</p>
            <input type="file" id="fileInput" accept="image/*">
        </div>
        
        <img id="image-preview">
        
        <div class="loading" id="loading">
            <p>Processing image...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <h3>Results:</h3>
            <div id="resultsList"></div>
        </div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const imagePreview = document.getElementById('image-preview');
        const loading = document.getElementById('loading');
        const error = document.getElementById('error');
        const results = document.getElementById('results');
        const resultsList = document.getElementById('resultsList');

        // File upload handler
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#4CAF50';
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = '#ccc';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileInput.files = e.dataTransfer.files;
            handleFile();
        });
        
        fileInput.addEventListener('change', handleFile);

        async function handleFile() {
            const file = fileInput.files[0];
            if (!file) return;

            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);

            // Send to API
            loading.style.display = 'block';
            error.style.display = 'none';
            results.style.display = 'none';

            try {
                const formData = new FormData();
                formData.append('file', file);

                const response = await fetch('http://127.0.0.1:8000/detect/image', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Access-Control-Allow-Origin': '*'
                    }
                });

                const result = await response.json();
                displayResults(result);
            } catch (err) {
                error.textContent = 'Error: ' + err.message;
                error.style.display = 'block';
            } finally {
                loading.style.display = 'none';
            }
        }

        function displayResults(data) {
            resultsList.innerHTML = '';
            
            const heading = document.createElement('h4');
            heading.textContent = `Total faces: ${data.total_faces}`;
            resultsList.appendChild(heading);

            data.detections.forEach((det, i) => {
                const item = document.createElement('div');
                item.className = 'result-item';
                item.innerHTML = `
                    <strong>Face ${i + 1}:</strong><br>
                    Emotion: <strong>${det.emotion}</strong> (${(det.emotion_confidence * 100).toFixed(1)}%)<br>
                    Position: (${det.bbox.x1}, ${det.bbox.y1}) to (${det.bbox.x2}, ${det.bbox.y2})<br>
                    Detection Confidence: ${(det.confidence * 100).toFixed(1)}%
                `;
                resultsList.appendChild(item);
            });

            results.style.display = 'block';
        }
    </script>
</body>
</html>
"""

# ============================================================================
# Example 7: Using with Flask Web App (Python)
# ============================================================================

FLASK_EXAMPLE = """
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:8000/detect/image"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    files = {'file': file}
    response = requests.post(API_URL, files=files)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
"""

# ============================================================================
# Example 8: Using with cURL (Command Line)
# ============================================================================

CURL_EXAMPLES = """
# Detect faces in an image
curl -X POST \\
  -F "file=@photo.jpg" \\
  http://127.0.0.1:8000/detect/image

# Pretty print JSON response
curl -X POST \\
  -F "file=@photo.jpg" \\
  http://127.0.0.1:8000/detect/image | jq

# With base64 (on Linux/Mac)
curl -X POST \\
  -H "Content-Type: application/json" \\
  -d "{\\"image_base64\\": \\"$(base64 -w0 < photo.jpg)\\"}" \\
  http://127.0.0.1:8000/detect/base64

# Check health
curl http://127.0.0.1:8000/health | jq
"""


if __name__ == "__main__":
    print(__doc__)
    
    print("\n" + "="*70)
    print("Example 6: HTML + JavaScript Frontend")
    print("="*70)
    print(HTML_EXAMPLE)
    
    print("\n" + "="*70)
    print("Example 7: Flask Web App")
    print("="*70)
    print(FLASK_EXAMPLE)
    
    print("\n" + "="*70)
    print("Example 8: cURL Commands")
    print("="*70)
    print(CURL_EXAMPLES)
