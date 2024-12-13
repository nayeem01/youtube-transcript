import requests
from youtube_transcript_api import YouTubeTranscriptApi

# Proxy settings
proxy = {
    "http": "http://qpoldsoi:brqx16r6ghyw@173.0.9.70:5653",
    "https": "http://qpoldsoi:brqx16r6ghyw@173.0.9.70:5653",  # Use HTTP instead of HTTPS
}
# Custom requests session to disable SSL verification
session = requests.Session()
session.proxies = proxy
session.verify = False

# Fetch the transcript using the proxy and session with SSL disabled
try:
    # Make the request with the custom session
    transcript = YouTubeTranscriptApi.get_transcript("bvA5-ls3MtQ", proxies=proxy)
    print(transcript)
except Exception as e:
    print(f"Error occurred: {e}")
