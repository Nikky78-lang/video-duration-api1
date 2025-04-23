from flask import Flask, request, jsonify
import requests
import tempfile
import os
import moviepy.editor as mp

app = Flask(__name__)

@app.route('/duration', methods=['GET'])
def get_duration():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(requests.get(url).content)
            tmp_path = tmp.name

        clip = mp.VideoFileClip(tmp_path)
        duration = int(clip.duration)  # округлення вниз до цілого числа
        clip.close()
        os.remove(tmp_path)

        return jsonify({"duration": duration})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
