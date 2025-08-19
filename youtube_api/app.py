"""
NOTE:
This script uses the `youtube-transcript-api` third-party Python library to fetch subtitle/caption text for a given YouTube video. This method does NOT use the official YouTube Data API; instead, it works by scraping transcript data when publicly available.

The reason for using this solution is that the official YouTube Data API does not allow direct access to subtitle/caption text for arbitrary public videos due to copyright and security restrictions. Therefore, 'youtube-transcript-api' is used here to fulfill the assignment requirement to generate subtitle text.
"""

from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/get_subtitles/<video_id>')
def get_subtitles(video_id):
    try:
        api=YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        print(transcript.snippets[0].text)

        full_text=" ".join([entry.text for entry in transcript.snippets])
       
        return jsonify({
            "video_id": video_id,
            "subtitles": full_text,
            "subtitle_length": len(full_text),
            "language": transcript.language
        })
     
    except TranscriptsDisabled:
        return jsonify({"error": "Subtitles are disabled for this video"}), 400
    except NoTranscriptFound:
        return jsonify({"error": "No subtitles available for this video"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/test')
def test():
    """Test with a video that has subtitles"""
    return get_subtitles("D2cwvpJSBX4")  

if __name__ == '__main__':
    app.run(debug=True)