from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from pydantic import BaseModel

app = FastAPI()

class VideoURL(BaseModel):
    url: str

def extract_video_id(url: str) -> str:
    if 'v=' not in url:
        raise ValueError("Invalid YouTube URL")
    video_id = url.split("v=")[1].split("&")[0]
    return video_id

@app.post("/get-transcript/")
async def get_transcript(video: VideoURL):
    try:
        video_id = extract_video_id(video.url)
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['de', 'en'])
        
        formatter = JSONFormatter()
        formatted_text = formatter.format_transcript(transcript)
        
        return {"video_id": video_id, "transcript": formatted_text}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching transcript: " + str(e))

