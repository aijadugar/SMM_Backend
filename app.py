from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
CORS(app)

OPENAI_CLIENT = os.getenv("OPENAI_CLIENT")
CLIENT_MODEL = os.getenv("CLIENT_MODEL")

client = OpenAI(base_url='https://api.a4f.co/v1', api_key=OPENAI_CLIENT)

@app.route('/generate-link', methods=['POST'])
def generate_link():
    data = request.get_json()
    user_text = data.get('text', '')

    model = client.images.generate(model=CLIENT_MODEL, 
                                    prompt=user_text,
                                    n=1,
                                    response_format='url',
                                    size="1500x600"
    )

    img_url = model.data[0].url

    return jsonify({'link': img_url})

if __name__ == '__main__':
    app.run(debug=True)

