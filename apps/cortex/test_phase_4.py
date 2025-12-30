import os
from core.db import SessionLocal, VideoProject
from services.renderer import RenderService

def test_final_render():
    print("--- NexusStudio: Phase 4 Final Render ---")
    
    db = SessionLocal()
    # Get the latest analyzed project
    project = db.query(VideoProject).filter_by(status="analyzed").first()
    
    if not project:
        print("❌ No analyzed video found. Please re-run Phase 2!")
        return

    try:
        renderer = RenderService()
        
        # Render the first segment (Index 0)
        print(f"🚀 Processing Best Clip from: {project.title}")
        output_path = renderer.render_segment(project, segment_index=0)
        
        print(f"\n🎉 SUCCESS! Viral Video Generated:")
        print(f"📂 {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"❌ Render Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_final_render()