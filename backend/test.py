proxies = {
    "http": "http://51.158.123.35:8811",  # Example free proxy IP
    "https": "http://51.158.123.35:8811",  # Example free proxy IP
}

# Use the proxy in your FastAPI app for YouTubeTranscriptAPI requests
import requests
from youtube_transcript_api import YouTubeTranscriptApi

session = requests.Session()
session.proxies.update(proxies)

YouTubeTranscriptApi._requests_session = session

# Test with a video ID
video_id = "bvA5-ls3MtQ"
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
print(transcript)
