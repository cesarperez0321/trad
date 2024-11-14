# app.py
from flask import Flask, request, jsonify
import openai
import os
import tempfile
import requests

app = Flask(__name__)

# Configura tu clave de API de OpenAI usando una variable de entorno
openai.api_key = os.getenv(' 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')

@app.route('/translate', methods=['POST'])
def translate():
    if 'audio' not in request.files or 'language' not in request.form:
        return jsonify({'error': 'Archivo de audio y idioma objetivo son requeridos.'}), 400

    audio_file = request.files['audio']
    target_language = request.form['language']

    try:
        # Guardar el archivo de audio en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.webm') as temp_audio:
            audio_file.save(temp_audio.name)

            # Transcribir el audio usando Whisper
            with open(temp_audio.name, 'rb') as audio:
                transcript = openai.Audio.transcribe("whisper-1", audio)
            original_text = transcript['text']
            detected_language = transcript['language']

            # Traducir el texto usando GPT-3.5 Turbo
            messages = [
                {"role": "system", "content": f"Eres un traductor que convierte texto del {detected_language} al {target_language}."},
                {"role": "user", "content": original_text}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.5,
            )
            translated_text = response['choices'][0]['message']['content'].strip()

            # Enviar la respuesta al frontend
            return jsonify({'translatedText': translated_text})

    except Exception as e:
        print('Error al procesar la traducción:', e)
        return jsonify({'error': 'Error al procesar la traducción.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
