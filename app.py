from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from bark import generate_audio, preload_models
from scipy.io.wavfile import write
import tempfile, glob

app = FastAPI()
preload_models()

@app.post("/speak")
async def speak(req: Request):
    data = await req.json()
    text = data.get("text", "")
    if not text:
        return {"error": "Missing 'text'"}
    wav = generate_audio(text)
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(f.name, 24000, wav)
    return {"url": "/audio.wav"}

@app.get("/audio.wav")
def audio():
    files = sorted(glob.glob("/tmp/*.wav"), key=lambda x: os.path.getctime(x), reverse=True)
    return FileResponse(files[0], media_type="audio/wav", filename="output.wav")
