from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from pydantic import BaseModel
import requests

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

proxies = {
    "http": "http://51.158.123.35:8811",
    "https": "http://51.158.123.35:8811",
}

session = requests.Session()
session.proxies.update(proxies)

YouTubeTranscriptApi._requests_session = session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


class VideoURL(BaseModel):
    url: str


def extract_video_id(url: str) -> str:
    if "v=" not in url:
        raise ValueError("Invalid YouTube URL")
    video_id = url.split("v=")[1].split("&")[0]
    return video_id


@app.post("/get-transcript/")
async def get_transcript(video: VideoURL):
    try:
        video_id = extract_video_id(video.url)
        logger.info(f"Fetching transcript for video: {video_id}")

        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["en"],
        )

        formatter = JSONFormatter()
        formatted_text = formatter.format_transcript(transcript)

        logger.error(f"text {formatted_text}")

        return {"video_id": video_id, "transcript": formatted_text}

    except ValueError as ve:
        logger.error(f"Invalid URL: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error fetching transcript for {video.url}: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error fetching transcript: " + str(e)
        )
