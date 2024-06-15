from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    audio_file = request.files['file']
    recognizer = sr.Recognizer()

    # Save the audio file temporarily
    audio_path = os.path.join('uploads', 'temp.wav')
    audio_file.save(audio_path)

    # Convert speech to text
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return jsonify({"error": "Google Speech Recognition could not understand audio"})
        except sr.RequestError as e:
            return jsonify({"error": f"Could not request results; {e}"})

    # Translate text
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='es').text

    # Convert text to speech
    engine = pyttsx3.init()
    engine.save_to_file(translated_text, 'output.mp3')
    engine.runAndWait()

    # Convert audio to base64 for sending in response
    with open('output.mp3', 'rb') as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    return jsonify({"translated_text": translated_text, "audio_base64": audio_base64})

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
