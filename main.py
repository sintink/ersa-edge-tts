from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import edge_tts

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Server Edge TTS Ersa Aktif!"}

@app.get("/tts")
async def generate_tts(text: str, voice: str = "id-ID-GadisNeural"):
    if not text:
        return Response(content="Teks tidak boleh kosong", status_code=400)
    
    communicate = edge_tts.Communicate(text, voice)
    audio_data = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
            
    return Response(content=bytes(audio_data), media_type="audio/mpeg")
  
