from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.db import SessionLocal, VideoProject, get_db
from services.ingestion import IngestionService
from services.brain import BrainService
from services.renderer import RenderService

app = FastAPI(title="Nexus Cortex")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Tauri/React to talk to Python
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class VideoRequest(BaseModel):
    url: str

@app.post("/ingest")
def ingest_video(request: VideoRequest):
    db = SessionLocal()
    service = IngestionService(db)
    try:
        project = service.process_video(request.url)
        return {"id": project.id, "title": project.title, "status": project.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/analyze/{video_id}")
def analyze_video(video_id: str):
    db = SessionLocal()
    service = BrainService(db)
    try:
        result = service.analyze_video(video_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/render/{video_id}/{segment_index}")
def render_video(video_id: str, segment_index: int):
    db = SessionLocal()
    try:
        project = db.query(VideoProject).filter_by(id=video_id).first()
        renderer = RenderService()
        output_path = renderer.render_segment(project, segment_index)
        return {"path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)