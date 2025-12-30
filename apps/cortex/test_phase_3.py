import cv2
import os
from core.db import SessionLocal, VideoProject
from vision.camera_operator import VirtualCameraman

def test_vision():
    print("--- NexusStudio: Phase 3 Vision Test ---")
    
    # 1. Load the video we downloaded in Phase 2
    # NOTE: You might need to check your database or folder for the exact filename
    # For this test, we grab the most recent one from the DB
    db = SessionLocal()
    project = db.query(VideoProject).order_by(VideoProject.created_at.desc()).first()
    db.close()
    
    if not project:
        print("❌ No video found in DB. Run Phase 2 first!")
        return

    print(f"🎥 Analyzing: {project.file_path}")
    
    cap = cv2.VideoCapture(project.file_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Setup Cameraman
    cameraman = VirtualCameraman(width, height)
    
    # Setup Output Video (Debug Mode)
    output_path = project.file_path.replace(".mp4", "_debug_crop.mp4").replace(".webm", "_debug_crop.mp4")
    # Using 'mp4v' codec for simple preview
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    frame_count = 0
    max_frames = 300 # Only process first 10 seconds for speed
    
    print("👁️  Processing frames (Limit: 300)...")
    
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        # 1. Ask Cameraman where to look
        center_x = cameraman.process_frame(frame)
        
        # 2. Get Coordinates
        x1, y1, x2, y2 = cameraman.get_crop_coordinates(center_x)
        
        # 3. Draw the "Debug Box" (Green Rectangle)
        # This shows us exactly what the vertical video will look like
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
        cv2.circle(frame, (center_x, height//2), 10, (0, 0, 255), -1) # Red dot = Center
        
        out.write(frame)
        frame_count += 1
        
        if frame_count % 50 == 0:
            print(f"   Processed {frame_count} frames...")
            
    cap.release()
    out.release()
    print(f"✅ Debug Video Saved: {output_path}")
    print("👉 Go open that file and check if the Green Box follows the face smoothly!")

if __name__ == "__main__":
    test_vision()