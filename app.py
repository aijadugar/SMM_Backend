from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from serpapi import GoogleSearch
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "https://smm-backend-wljg.onrender.com",
    "https://thesmmhub.vercel.app"
])

OPENAI_CLIENT = os.getenv("OPENAI_CLIENT")
CLIENT_MODEL = os.getenv("CLIENT_MODEL")
SERP_API = os.getenv('SERP_API')

client = OpenAI(base_url='https://api.a4f.co/v1', api_key=OPENAI_CLIENT)

@app.route('/generate-link', methods=['POST'])
def generate_link():
    data = request.get_json()
    user_text = data.get('text', '')

    try:
        model = client.images.generate(
            model=CLIENT_MODEL,
            prompt=user_text,
            n=1,
            response_format='url',
            size="1500x600"
        )

        img_url = model.data[0].url
        return jsonify({'link': img_url})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({'link': 'Error generating image.'}), 500

@app.route('/hashtags', methods=['POST'])
def get_hashtag_suggestions():
    data = request.get_json()
    topic = data.get('topic', '')
    print(f"🔍 Topic received: {topic}")

    params = {
        "engine": "google_autocomplete",
        "q": topic,
        "api_key": SERP_API,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    print("📦 SerpApi response:", results)

    hashtags = []
    for item in results.get("suggestions", []):
        keyword = item.get("value") or item.get("suggestion")
        if keyword:
            hashtag = "#" + keyword.lower().replace(" ", "")
            hashtags.append(hashtag)

    print("✅ Hashtags generated:", hashtags)

    return jsonify({'hashtags': hashtags})

if __name__ == '__main__':
    app.run(debug=True)
