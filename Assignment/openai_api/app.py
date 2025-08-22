"""
NOTE:
This script uses Google Gemini (via the google-generativeai library) to perform GPT-style summarization of YouTube video transcripts.
Originally, OpenAI's GPT API was considered, but due to insufficient quota/no free credits available for new accounts, the implementation was switched to Google Gemini, which currently provides a free API tier for developers and students.
"""
import os
from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/summary')
def summarize_video():
    video_id = "D2cwvpJSBX4"  
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        print(transcript.snippets[0].text)
        full_text = " ".join([entry.text for entry in transcript.snippets])

        prompt = (
            "Summarize this YouTube transcript in 5 bullet points:\n\n"
            f"{full_text}"
        )
        response = model.generate_content(prompt)
        summary = response.text
        return jsonify({"video_id": video_id, "summary": summary, "transcript_length": len(full_text)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
