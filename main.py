from flask import Flask, request, jsonify
import moviepy.editor as mp
import os
import tempfile

app = Flask(__name__)

def seconds_to_hms(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"

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
        duration_seconds = video.duration
        duration_hms = seconds_to_hms(duration_seconds)

        os.remove(temp_file_path)
        return jsonify({'duration': duration_hms})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
