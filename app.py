from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from bark import generate_audio, preload_models
from scipy.io.wavfile import write
import tempfile, glob, os

app = FastAPI()
preload_models()

@app.post("/speak")
async def speak(req: Request):
    data = await req.json()
    text = data.get("text", "")
    if not text:
        return {"error": "Missing 'text'"}
    audio_array = generate_audio(text)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp.name, 24000, audio_array)
    return {"url": "/audio.wav"}

@app.get("/audio.wav")
def audio():
    files = sorted(glob.glob("/tmp/*.wav"), key=os.path.getctime, reverse=True)
    return FileResponse(files[0], media_type="audio/wav", filename="output.wav")
