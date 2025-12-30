import os
import yt_dlp
from faster_whisper import WhisperModel
from sqlalchemy.orm import Session
from core.db import VideoProject
from config.settings import settings

class IngestionService:
    def __init__(self, db: Session):
        self.db = db
        self.data_dir = os.path.join(settings.project_root or "../..", "data", "input")
        os.makedirs(self.data_dir, exist_ok=True)

    def process_video(self, url: str):
        print(f"🚀 Starting Ingestion for: {url}")
        
        # Download
        video_path, audio_path, info = self._download(url)
        video_id = info['id']
        
        # Check DB (Idempotency)
        existing = self.db.query(VideoProject).filter_by(id=video_id).first()
        if existing and existing.status == "analyzed":
            print("✅ Video already processed.")
            return existing

        if not existing:
            project = VideoProject(
                id=video_id,
                title=info['title'],
                url=url,
                file_path=video_path,
                audio_path=audio_path,
                status="downloaded"
            )
            self.db.add(project)
            self.db.commit()
        else:
            project = existing

        # Transcribe (CPU Optimized)
        if project.status != "transcribed" and project.status != "analyzed":
            print("🎙️ Starting Transcription (This may take a moment on CPU)...")
            transcript_data = self._transcribe(audio_path)
            
            project.transcript_json = transcript_data
            project.status = "transcribed"
            self.db.commit()
            print(f"✅ Transcription Complete: {len(transcript_data)} segments found.")
            
        return project

    def _download(self, url: str):
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]', # 720p is enough for AI analysis, saves bandwidth
            'outtmpl': os.path.join(self.data_dir, '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav', # WAV is faster for Whisper than MP3
            }],
            'keepvideo': True, 
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = os.path.join(self.data_dir, f"{info['id']}.mp4")
            audio_path = os.path.join(self.data_dir, f"{info['id']}.wav")
            # If mp4 doesn't exist (merged), check mkv or webm
            if not os.path.exists(video_path):
                video_path = os.path.join(self.data_dir, f"{info['id']}.mkv")
                
        return video_path, audio_path, info

    def _transcribe(self, audio_path: str):
        model = WhisperModel("small", device="cpu", compute_type="int8")
        
        segments, info = model.transcribe(audio_path, beam_size=5)
        
        # Convert generator to list of dicts for JSON storage
        results = []
        for segment in segments:
            results.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
            
        return results