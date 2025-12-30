import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, JSON, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import settings

DB_FOLDER = os.path.join(settings.project_root or "../..", "data", "db")
os.makedirs(DB_FOLDER, exist_ok=True)
DB_PATH = f"sqlite:///{os.path.join(DB_FOLDER, 'nexus.sqlite')}"

Base = declarative_base()


class VideoProject(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)  # YouTube ID or Hash
    title = Column(String)
    url = Column(String)
    file_path = Column(String)  # Local path to .mp4
    audio_path = Column(String)
    transcript_json = Column(JSON)
    # Analysis from the "Brain"
    summary = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(
        String, default="pending"
    )  # pending, downloaded, transcribed, analyzed


engine = create_engine(DB_PATH)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
