from flask import Flask, request, jsonify
import requests  # <-- Додано цей імпорт
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
        content = requests.get(url).content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file.write(content)
            video = mp.VideoFileClip(temp_file.name)
            os.remove(temp_file_path)
            return jsonify(video.duration)
        return jsonify(0)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'url': url,
            'content': content
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
