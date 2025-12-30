import cv2
import os
import subprocess
from core.db import VideoProject
from vision.camera_operator import VirtualCameraman
from services.subtitles import generate_karaoke_subtitles


class RenderService:
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or os.path.join("..", "..", "data", "output")
        os.makedirs(self.output_dir, exist_ok=True)

    def render_segment(self, project: VideoProject, segment_index: int):
        # 1. Get Segment Data
        if not project.summary:
            raise ValueError("Video has not been analyzed by the Brain.")

        import json

        analysis = json.loads(project.summary)
        segment = analysis["segments"][segment_index]

        start_time = segment["start_time"]
        end_time = segment["end_time"]
        duration = end_time - start_time
        safe_title = (
            "".join([c for c in segment["title"] if c.isalnum() or c == " "])
            .strip()
            .replace(" ", "_")
        )

        print(f"🎬 Rendering: {segment['title']}")
        print(f"⏱️  Time: {start_time}s - {end_time}s")

        # 2. Setup Paths
        abs_input_path = os.path.abspath(project.file_path)

        if not os.path.exists(abs_input_path):
            raise FileNotFoundError(
                f"CRITICAL: Source video missing at {abs_input_path}"
            )

        temp_video_path = os.path.abspath(
            os.path.join(self.output_dir, "temp_video.mp4")
        )
        temp_audio_path = os.path.abspath(
            os.path.join(self.output_dir, "temp_audio.aac")
        )
        final_output_path = os.path.abspath(
            os.path.join(self.output_dir, f"{safe_title}.mp4")
        )

        # ... (OpenCV section uses abs_input_path instead of project.file_path)
        cap = cv2.VideoCapture(abs_input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Validation: Check if video is long enough
        if end_time * fps > total_frames:
            print(
                f"⚠️ Warning: Clip end time ({end_time}s) exceeds video duration. Clamping."
            )
            end_time = total_frames / fps

        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # Init Cameraman
        cameraman = VirtualCameraman(width, height)

        # Output Writer
        target_h = 1920
        target_w = 1080
        out = cv2.VideoWriter(
            temp_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (target_w, target_h)
        )

        current_frame = start_frame

        print("⚙️  Generating Frames (Visuals)...")
        while cap.isOpened() and current_frame < end_frame:
            ret, frame = cap.read()
            if not ret:
                break

            center_x = cameraman.process_frame(frame)
            x1, y1, x2, y2 = cameraman.get_crop_coordinates(center_x)
            crop_img = frame[y1:y2, x1:x2]
            final_frame = cv2.resize(
                crop_img, (target_w, target_h), interpolation=cv2.INTER_CUBIC
            )

            out.write(final_frame)
            current_frame += 1

            if current_frame % 30 == 0:
                print(
                    f"   Rendered {current_frame - start_frame} / {end_frame - start_frame} frames",
                    end="\r",
                )

        cap.release()
        out.release()
        print("\n✅ Video Track Complete.")

        print("📝 Generating Subtitles...")
        subtitle_path = os.path.join(self.output_dir, "subtitles.ass")
        # Ensure we pass the absolute path for FFmpeg
        abs_subtitle_path = os.path.abspath(subtitle_path).replace("\\", "/")
        # Note: FFmpeg on Windows is picky about paths in filtergraphs. Forward slashes help.

        generate_karaoke_subtitles(
            project.transcript_json, start_time, end_time, subtitle_path
        )

        # 4. AUDIO PROCESSING (FFmpeg)
        print("🔊 Extracting Audio...")
        # REMOVED: stdout=subprocess.DEVNULL (So we can see errors)
        # ADDED: check=True (So it stops if it fails)
        try:
            # FIXED: Passing absolute paths to FFmpeg
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    abs_input_path,
                    "-ss",
                    str(start_time),
                    "-t",
                    str(duration),
                    "-vn",
                    "-acodec",
                    "aac",
                    temp_audio_path,
                ],
                check=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            print(f"\n❌ FFmpeg Audio Error:\n{e.stderr.decode()}")
            raise e

        # 5. MERGE (Muxing)
        print("✨ Merging Final Cut...")
        escaped_sub_path = abs_subtitle_path.replace(":", "\\:")
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    temp_video_path,
                    "-i",
                    temp_audio_path,
                    "-vf",
                    f"subtitles='{escaped_sub_path}'",  # <--- The Magic Line
                    "-c:v",
                    "libx264",  # Must re-encode video to burn text
                    "-preset",
                    "fast",
                    "-c:a",
                    "aac",
                    final_output_path,
                ],
                check=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            print(f"\n❌ FFmpeg Subtitle Merge Error:\n{e.stderr.decode()}")
            raise e

        # Cleanup
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

        return final_output_path
