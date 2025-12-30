from core.db import SessionLocal
from services.ingestion import IngestionService
from services.brain import BrainService

def test_brain():
    print("--- NexusStudio: Phase 2 Brain Test ---")
    
    # Use the SAME video URL as Phase 1 (it will skip download/transcribe because of DB check)
    TEST_URL = "https://www.youtube.com/watch?v=r6zFZQm0hcc" 
    
    db = SessionLocal()
    
    try:
        # 1. Ensure we have the data (Ingest again just to get the project object)
        ingestor = IngestionService(db)
        project = ingestor.process_video(TEST_URL)
        
        # 2. Run the Brain
        brain = BrainService(db)
        analysis = brain.analyze_video(project.id)
        
        # 3. Print the Result
        print("\n🤖 AI Director's Report:")
        print(f"Summary: {analysis.get('summary')}")
        print("\n🎬 Suggested Viral Clips:")
        for clip in analysis.get('segments', []):
            print(f"   Title: {clip['title']}")
            print(f"   Score: {clip['virality_score']}/100")
            print(f"   Time:  {clip['start_time']}s -> {clip['end_time']}s")
            print(f"   Why:   {clip['reasoning']}\n")
            
    except Exception as e:
        print(f"❌ Critical Failure: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_brain()