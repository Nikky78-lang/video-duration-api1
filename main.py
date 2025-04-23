
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/api/get-duration", methods=["GET"])
def get_duration():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            url
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        duration = float(result.stdout.strip())
        return jsonify({"duration": duration})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(host="0.0.0.0", port=10000)
