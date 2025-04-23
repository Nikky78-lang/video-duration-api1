from flask import Flask, request, jsonify
import requests  # <-- Додано цей імпорт
import moviepy.editor as mp
import os
import tempfile

app = Flask(__name__)

@app.route('/duration')
def get_duration():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file.write(requests.get(url).content)
            temp_file_path = temp_file.name

        video = mp.VideoFileClip(temp_file_path)
        os.remove(temp_file_path)
        return jsonify(video.duration)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
