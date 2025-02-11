#!/usr/bin/env python3

import cv2
import torch
from transformers import AutoProcessor, CLIPModel
import numpy as np
from datetime import datetime

class SmartCamera:
    def __init__(self):
        # Initialize CLIP model
        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32",
            torch_dtype=torch.float16
        )
        self.processor = AutoProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        
    def process_frame(self, frame, text_queries):
        """Process frame with CLIP model"""
        # Prepare image
        inputs = self.processor(
            images=frame,
            text=text_queries,
            return_tensors="pt",
            padding=True
        )
        
        # Get predictions
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        
        return probs.detach().numpy()
    
    def run(self, text_queries=["person", "car", "dog", "cat"]):
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break
                
            # Process frame
            probs = self.process_frame(frame, text_queries)
            
            # Draw results
            for i, query in enumerate(text_queries):
                prob = probs[0][i]
                if prob > 0.5:  # Confidence threshold
                    text = f"{query}: {prob:.2f}"
                    cv2.putText(
                        frame,
                        text,
                        (10, 30 + i*30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )
            
            # Display frame
            cv2.imshow('Smart Camera', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    camera = SmartCamera()
    camera.run()
