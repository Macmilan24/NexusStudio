import numpy as np
import cv2
# CHANGED: Explicit imports to bypass "lazy loading" issues
import mediapipe as mp
from mediapipe.python.solutions import face_mesh

class VirtualCameraman:
    def __init__(self, video_width, video_height):
        self.video_width = video_width
        self.video_height = video_height
        
        # Target Dimensions (9:16 Vertical)
        self.target_height = video_height
        self.target_width = int(self.target_height * (9 / 16))
        
        # Physics State
        self.current_x = video_width // 2  # Start center
        
        # --- THE SECRET SAUCE (Tunable Physics) ---
        self.dead_zone = 50 
        self.smooth_factor = 0.05 
        
        # CHANGED: Use the direct import
        self.face_mesh = face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

    def process_frame(self, frame):
        """
        Input: A raw video frame (numpy array)
        Output: The top-left X coordinate for the crop
        """
        # 1. Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        target_x = self.current_x

        # 2. Did we find a face?
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            
            # Get Nose Tip (Landmark #1)
            nose_x = int(landmarks[1].x * self.video_width)
            
            # Update Target
            target_x = nose_x

        # 3. Apply "Cinematic Damping"
        return self._apply_physics(target_x)

    # ... (Rest of the class remains exactly the same: _apply_physics, _clamp_crop, get_crop_coordinates)
    def _apply_physics(self, face_x):
        diff = face_x - self.current_x
        if abs(diff) < self.dead_zone:
            return self._clamp_crop(self.current_x)
        self.current_x += diff * self.smooth_factor
        return self._clamp_crop(self.current_x)

    def _clamp_crop(self, center_x):
        half_width = self.target_width // 2
        if center_x - half_width < 0:
            return half_width
        if center_x + half_width > self.video_width:
            return self.video_width - half_width
        return int(center_x)

    def get_crop_coordinates(self, center_x):
        x1 = int(center_x - (self.target_width // 2))
        y1 = 0
        x2 = x1 + self.target_width
        y2 = self.target_height
        return x1, y1, x2, y2