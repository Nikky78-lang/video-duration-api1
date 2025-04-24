from flask import Flask, request, jsonify
import requests
import moviepy.editor as mp
import os
import tempfile
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/duration')
def get_duration():
    url = unquote(request.args.get('url'))
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        # Скачуємо відео
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Визначаємо розширення (mp4 як дефолт)
        ext = os.path.splitext(url)[1]
        if ext not in ['.mp4', '.mov', '.webm']:
            ext = '.mp4'

        # Зберігаємо тимчасовий файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name

        # Отримуємо тривалість
        video = mp.VideoFileClip(temp_path)
        duration = round(video.duration, 3)
        video.close()
        os.remove(temp_path)

        return jsonify(duration)

    except Exception as e:
        return jsonify({'error': str(e), 'url': url}), 500

if __name__ == '__main__':
    app.run(debug=True)
