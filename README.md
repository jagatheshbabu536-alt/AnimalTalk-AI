# AnimalTalk AI — Dog + Cat Sound to Tamil

A Flask web app that sends an uploaded dog/cat audio clip to the Gemini API for cautious sound interpretation, displays the response in Tamil, and reads the Tamil text aloud using the browser's speech synthesis.

## What it does
- Select Dog or Cat.
- Upload WAV, MP3, M4A, AAC, OGG, FLAC, WEBM or AIFF (up to 20 MB).
- Gemini analyses the audio and produces a cautious Tamil interpretation.
- Tamil Text-to-Speech button uses the browser's installed Tamil voice when available.
- Copy and stop-speaking controls.

## Important scientific limitation
This is an AI-generated interpretation of animal vocalizations, not a literal animal-language translator. There is no scientifically validated universal dog/cat-to-human translation system. The model is instructed to describe plausible meaning, audible evidence and uncertainty, and to abstain when audio is unclear. Do not use it for medical or emergency decisions.

## Setup on Windows / VS Code

1. Extract the ZIP and open the `AnimalTalk_AI_Dog_Cat` folder in VS Code.
2. Open a terminal in that folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

4. Install packages:

   ```powershell
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to a new file named `.env`.
6. Get a Gemini API key from Google AI Studio and paste it into `.env`:

   ```env
   GEMINI_API_KEY=your_actual_key_here
   GEMINI_MODEL=gemini-3.8-flash
   ```

   Keep `.env` private. Do not upload it to GitHub or share it.

7. Start the website:

   ```powershell
   python app.py
   ```

8. Open `http://127.0.0.1:5000` in your browser.

## Tamil voice
The browser's Web Speech API is used for speech output. Tamil voice availability depends on the operating system and browser. If no Tamil voice is installed, the text still appears; install/enable a Tamil speech voice in your OS/browser settings.

## Troubleshooting
- **API key missing:** confirm `.env` exists beside `app.py`, and the key line has no quotes or extra spaces.
- **Model not found / unavailable:** change `GEMINI_MODEL` to a currently available audio-capable model in your Google AI Studio project.
- **Quota or billing error:** check API quota and billing/availability in Google AI Studio.
- **Audio rejected:** try a short, clear recording in WAV or MP3, under 20 MB.
- **No Tamil voice:** browser speech synthesis depends on installed voices; try another browser or enable a Tamil voice in system settings.

## Project structure

```text
AnimalTalk_AI_Dog_Cat/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── uploads/
    └── .gitkeep
```
