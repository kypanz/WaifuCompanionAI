# n8n_kokoro_server.py
from flask import Flask, request
import torch
import numpy as np
from kokoro import KPipeline
import soundfile as sf
import subprocess
import tempfile
import os

app = Flask(__name__)

# Pipeline cargado en GPU una sola vez
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Usando dispositivo: {device}")
pipeline = KPipeline(lang_code='a') # a = english | e = spanish
print("Pipeline cargado en GPU ✅")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    if not text:
        return {"error": "No text provided"}, 400

    # Generar audio por chunks y reproducir en tiempo real
    generator = pipeline(text, voice='af_sky') # Modelos aqui
    for i, (gs, ps, audio) in enumerate(generator):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            sf.write(tmpfile.name, audio, 24000)
            subprocess.run(["paplay", "--device=VirtualMic", tmpfile.name])
            os.unlink(tmpfile.name)

    return {"status": "ok", "message": "Audio reproducido en VirtualMic"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
