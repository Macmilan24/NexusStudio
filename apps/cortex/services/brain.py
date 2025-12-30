import json
from sqlalchemy.orm import Session
from core.db import VideoProject
from core.llm_factory import LLMFactory
from agents.prompts import NARRATIVE_ARCHITECT_PROMPT
from langchain_core.output_parsers import JsonOutputParser

class BrainService:
    def __init__(self, db: Session):
        self.db = db
        # We use the "Brain" (Gemini/OpenRouter) because we need a large context window
        self.llm = LLMFactory.get_brain() 

    def analyze_video(self, video_id: str):
        print(f"🧠 Brain Activated: Analyzing {video_id}...")
        
        project = self.db.query(VideoProject).filter_by(id=video_id).first()
        if not project or not project.transcript_json:
            raise ValueError("Video not found or transcript missing.")

      
        readable_transcript = "\n".join(
            f"[{seg['start']:.1f}s] {seg['text']}" 
            for seg in project.transcript_json
        )

        # 3. Invoke the Agent
        chain = NARRATIVE_ARCHITECT_PROMPT | self.llm | JsonOutputParser()
        
        try:
            analysis_result = chain.invoke({"transcript_text": readable_transcript})
        
            print("✅ Analysis Complete!")
            
            project.summary = json.dumps(analysis_result) 
            project.status = "analyzed"
            self.db.commit()
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ Brain Error: {e}")
            raise e