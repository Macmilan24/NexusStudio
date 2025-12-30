from core.db import SessionLocal
from services.ingestion import IngestionService

def test_ingestion():
    print("--- NexusStudio: Phase 1 Ingestion Test ---")
    
    # Use a short video for testing (approx 1 min) to save time
    # This is a random copyright-free test video
    TEST_URL = "https://www.youtube.com/watch?v=zBjJUV-lzHo" 
    
    db = SessionLocal()
    ingestor = IngestionService(db)
    
    try:
        project = ingestor.process_video(TEST_URL)
        
        print(f"\n🎥 Video: {project.title}")
        print(f"📂 Path: {project.file_path}")
        print(f"📝 Transcript Preview (First 2 lines):")
        
        # Safe access to JSON
        if project.transcript_json:
            for seg in project.transcript_json[:2]:
                print(f"   [{seg['start']:.1f}s - {seg['end']:.1f}s]: {seg['text']}")
        else:
            print("❌ No transcript found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_ingestion()