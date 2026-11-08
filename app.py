import os
import mimetypes
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac", ".webm", ".aiff"}
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

def allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/analyze")
def analyze():
    animal = request.form.get("animal", "dog").strip().lower()
    audio = request.files.get("audio")

    if animal not in {"dog", "cat"}:
        return jsonify({"error": "Dog அல்லது Cat தேர்வு செய்யவும்."}), 400
    if not audio or not audio.filename:
        return jsonify({"error": "முதலில் audio file upload செய்யவும்."}), 400
    if not allowed_file(audio.filename):
        return jsonify({"error": "WAV, MP3, M4A, AAC, OGG, FLAC அல்லது WEBM audio file பயன்படுத்தவும்."}), 400

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return jsonify({"error": "Gemini API key அமைக்கப்படவில்லை. Project folder-ல் உள்ள .env file-ல் GEMINI_API_KEY சேர்த்து மீண்டும் run செய்யவும்."}), 400

    try:
        audio_bytes = audio.read()
        if not audio_bytes:
            return jsonify({"error": "Audio file காலியாக உள்ளது."}), 400

        mime_type = audio.mimetype or mimetypes.guess_type(audio.filename)[0] or "audio/wav"
        client = genai.Client(api_key=api_key)

        animal_name = "நாய்" if animal == "dog" else "பூனை"
        prompt = f"""
You are AnimalTalk AI, a cautious animal-vocalization interpretation assistant.
The uploaded audio is said to be from a {animal} ({animal_name}).

Analyze the actual sound in the audio. Do NOT pretend animals speak human words
or claim to know their exact thoughts. Animal vocalizations do not have a proven
direct word-for-word human translation. Infer only a plausible communication
function or state from audible evidence, and be conservative.

Reply ONLY in Tamil using these headings:
சாத்தியமான அர்த்தம்:
[One or two simple Tamil sentences. If uncertain, say so clearly.]

ஒலி ஆதாரம்:
[Describe audible features such as repeated barking/meowing, pitch, duration,
rhythm, intensity, pauses. Do not invent features.]

நம்பகத்தன்மை:
[Low / Medium / High, with a short reason. Do not give a numeric accuracy
percentage. If species/source cannot be identified confidently, say that.]

கவனிக்க வேண்டியது:
[One practical, non-diagnostic suggestion. If the animal seems distressed,
recommend checking its environment and consulting a veterinarian when needed.]

Important:
- Do not treat human speech, music, or background noise as animal language.
- If the audio is unclear, too short, or not recognizably a {animal}, say
  "இந்த audio-வில் இருந்து நம்பகமான விளக்கம் தர முடியவில்லை."
- Never output a fabricated direct quote as if the animal literally said it.
- Be concise, kind, and understandable to a Tamil-speaking user.
"""
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                prompt,
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
            ],
        )
        result = (response.text or "").strip()
        if not result:
            return jsonify({"error": "AI-யிடமிருந்து விளக்கம் கிடைக்கவில்லை. வேறு audio try செய்யவும்."}), 502

        return jsonify({
            "result": result,
            "animal": animal,
            "model": MODEL_NAME,
            "note": "இது ஒலி அடிப்படையிலான சாத்தியமான விளக்கம் மட்டுமே; உறுதியான மொழிபெயர்ப்பு அல்ல."
        })
    except Exception as exc:
        # Keep the API key and internal details out of the browser response.
        app.logger.exception("Audio analysis failed")
        return jsonify({"error": "Audio analysis தோல்வியடைந்தது. API key, model availability, internet connection ஆகியவற்றைச் சரிபார்க்கவும். விவரம்: " + str(exc)[:240]}), 500

@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Audio file 20 MB-ஐ விடக் குறைவாக இருக்க வேண்டும்."}), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
