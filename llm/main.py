from flask import Flask, request, jsonify
from groq import Groq
import json

app = Flask(__name__)

client = Groq(api_key="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")

@app.route('/generate-questions', methods=['GET'])
def generate_questions():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({"error": "Missing topic"}), 400

    prompt = f"""
Generate 5 multiple-choice questions for the topic: "{topic}".
Return them strictly in this JSON format:
[
  {{
    "question": "string",
    "options": ["A", "B", "C", "D"],
    "correct_option": "B"
  }}
]
Do not add any explanations or additional text. Only return valid JSON.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Or any Groq-supported model like llama3-70b-8192
            messages=[
                {"role": "system", "content": "You are a quiz question generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON safely
        questions = json.loads(content)
        return jsonify({"topic": topic, "questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
