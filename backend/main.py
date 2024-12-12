from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from pydantic import BaseModel
import logging
import requests
import socks

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SOCKS5 proxy configuration (replace with your SOCKS5 proxy)
SOCKS_PROXY = "socks5h://qpoldsoi:brqx16r6ghyw@198.23.239.134:6540"  # Your SOCKS5 proxy

# Custom proxy setup using requests
session = requests.Session()
session.proxies = {
    "http": SOCKS_PROXY,
    "https": SOCKS_PROXY,
}

# FastAPI app setup
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
    """Extract the YouTube video ID from a URL."""
    if "v=" not in url:
        raise ValueError("Invalid YouTube URL")
    video_id = url.split("v=")[1].split("&")[0]
    return video_id


@app.post("/get-transcript/")
async def get_transcript(video: VideoURL):
    """Fetch and return the transcript for the provided YouTube video URL."""
    try:
        video_id = extract_video_id(video.url)
        logger.info(f"Fetching transcript for video: {video_id}")

        # Set the session with SOCKS proxy for the request
        YouTubeTranscriptApi.requests_session = session

        # Fetch the transcript using the API with the SOCKS5 proxy
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

        # Format the transcript to JSON
        formatter = JSONFormatter()
        formatted_text = formatter.format_transcript(transcript)

        logger.info(f"Successfully fetched transcript for {video_id}")

        return {"video_id": video_id, "transcript": formatted_text}

    except ValueError as ve:
        logger.error(f"Invalid URL: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error fetching transcript for {video.url}: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error fetching transcript: " + str(e)
        )
