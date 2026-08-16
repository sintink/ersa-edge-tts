from fastapi import FastAPI, WebSocket
import uvicorn
import asyncio
import edge_tts
import json
import os

app = FastAPI()
PORT = int(os.environ.get("PORT", 8080))

async def text_to_speech(text, output_file="output.mp3"):
    communicate = edge_tts.Communicate(text, "id-ID-GadisNeural")
    await communicate.save(output_file)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("ESP32 Berhasil Terhubung!")
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            user_text = message.get("text", "")
            print(f"Menerima dari ESP32: {user_text}")

            ai_response = f"Kamu bilang: {user_text}"
            
            await websocket.send_json({
                "type": "tts",
                "text": ai_response,
                "audio_url": "proses_audio"
            })
    except Exception as e:
        print(f"Koneksi terputus: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
    
