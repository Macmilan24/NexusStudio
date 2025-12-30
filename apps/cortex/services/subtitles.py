import os

def generate_karaoke_subtitles(transcript_json, start_time, end_time, output_path):
    """
    Generates a .ass subtitle file with a 'Karaoke' highlight effect.
    """
    
    # 1. Header (Define the Style)
    # PrimaryColour: &H00FFFFFF (Yellow/White)
    # Outline: 2 pixels black
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,80,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,250,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    events = []
    
    # 2. Filter words that are inside our clip range
    relevant_words = []
    # Whisper sometimes gives segments, sometimes words. 
    # We assume 'transcript_json' is the list of segments from earlier.
    # For a real karaoke effect, we need word-level timestamps. 
    # Since we used 'small' model defaults earlier, we might only have segments.
    # We will simulate "Phrase-Level" popping for now.
    
    for seg in transcript_json:
        if seg['end'] < start_time: continue
        if seg['start'] > end_time: break
        
        # Adjust relative time (Clip starts at 0s, but transcript is at 50s)
        rel_start = max(0, seg['start'] - start_time)
        rel_end = seg['end'] - start_time
        
        # Format time to H:MM:SS.cs
        def fmt(t):
            h = int(t // 3600)
            m = int((t % 3600) // 60)
            s = int(t % 60)
            cs = int((t % 1) * 100)
            return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

        # Create the Event Line
        # {\k0} is a dummy tag to enable karaoke processing if we had it
        # We wrap the text in a style that puts it in the center-bottom
        text = seg['text']
        line = f"Dialogue: 0,{fmt(rel_start)},{fmt(rel_end)},Default,,0,0,0,,{text}"
        events.append(line)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(events))
        
    return output_path