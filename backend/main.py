from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from pydantic import BaseModel
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import socks

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SOCKS5 Proxy setup
SOCKS_PROXY = "socks5h://qpoldsoi:brqx16r6ghyw@198.23.239.134:6540"

# Custom proxy session setup using requests and socks
session = requests.Session()


class SOCKSProxyAdapter(HTTPAdapter):
    """Adapter to use SOCKS proxy with requests."""

    def __init__(self, socks_proxy_url, **kwargs):
        self.socks_proxy_url = socks_proxy_url
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["proxy"] = self.socks_proxy_url
        kwargs["proxy_headers"] = {
            "Proxy-Authorization": f"Basic {self.socks_proxy_url.split('://')[1]}"
        }
        return super().init_poolmanager(*args, **kwargs)


# Mount the adapter to the session for both http and https
socks_adapter = SOCKSProxyAdapter(SOCKS_PROXY)
session.mount("http://", socks_adapter)
session.mount("https://", socks_adapter)

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
        # Extract video ID from URL
        video_id = extract_video_id(video.url)

        # Set the session with SOCKS proxy for YouTube Transcript API
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
