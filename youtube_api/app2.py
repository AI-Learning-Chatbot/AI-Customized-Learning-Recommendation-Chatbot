"""
NOTE:
The YouTube Data API does NOT provide access to actual subtitle/caption text for arbitrary videos due to privacy and copyright restrictions. Therefore, this script demonstrates the use of the official YouTube Data API (with API key) by fetching video metadata—specifically the title and description—for a given video, rather than subtitle text.
"""

from flask import Flask, jsonify
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()  

app2 = Flask(__name__)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@app2.route('/get_subtitles/<video_id>')
def get_subtitles(video_id):
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        video_data = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()
        
        snippet = video_data["items"][0]["snippet"]
        text_content = f"{snippet['title']}. {snippet['description']}"
        
        return jsonify({
            "video_id": video_id,
            "text": text_content,
            "text_length": len(text_content)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app2.route('/test')
def test():
    """Test with a sample video"""
    return get_subtitles("D2cwvpJSBX4")  

if __name__ == '__main__':
    app2.run(debug=True, port=5001)