# app/face_recognition.py
import numpy as np
from deepface import DeepFace
from PIL import Image
import io
import json
from typing import List, Tuple

class FaceService:
    def __init__(self, model_name='ArcFace', detector_backend='retinaface'):
        self.model_name = model_name
        self.detector_backend = detector_backend
        self.threshold = 0.6  # Similarity threshold
    
    def image_to_embedding(self, image_data) -> List[float]:
        """Convert image to facial embedding vector"""
        try:
            # Handle base64 or file upload
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                # Extract base64 data
                image_data = image_data.split(',')[1]
            
            if isinstance(image_data, str):
                # Base64 string
                import base64
                image_bytes = base64.b64decode(image_data)
                img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            else:
                # File upload
                img = Image.open(image_data.stream).convert('RGB')
            
            img_array = np.array(img)
            
            # Get face embedding
            representations = DeepFace.represent(
                img_array, 
                model_name=self.model_name, 
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            
            if not representations:
                raise ValueError("No face detected in image")
            
            return representations[0]['embedding']
            
        except Exception as e:
            raise ValueError(f"Face processing error: {str(e)}")
    
    def compare_faces(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Compare two face embeddings and return similarity score"""
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)
        
        # Cosine similarity
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
        
        return float(similarity)
    
    def verify_face(self, probe_embedding: List[float], stored_embeddings: List[List[float]]) -> Tuple[bool, float]:
        """Verify if probe face matches any stored embeddings"""
        best_score = 0
        for stored in stored_embeddings:
            score = self.compare_faces(probe_embedding, stored)
            if score > best_score:
                best_score = score
        
        return best_score >= self.threshold, best_score

# Global instance
face_service = FaceService()