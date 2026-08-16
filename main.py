from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import edge_tts
import json
import os

app = FastAPI()
PORT = int(os.environ.get("PORT", 8080))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[SERVER] ESP32 Berhasil Terhubung!")
    try:
        while True:
            # Terima teks dari ESP32
            data = await websocket.receive_text()
            message = json.loads(data)
            user_text = message.get("text", "")
            print(f"[SERVER] Menerima dari ESP32: {user_text}")

            if not user_text.strip():
                continue

            # Stream audio dari Edge TTS langsung ke ESP32
            communicate = edge_tts.Communicate(user_text, "id-ID-GadisNeural")
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    # Kirim potongan data MP3 (Binary) ke ESP32
                    await websocket.send_bytes(chunk["data"])

            # Kirim sinyal penanda audio selesai (Text JSON)
            await websocket.send_json({"status": "end"})
            print("[SERVER] Audio selesai dikirim ke ESP32!")

    except WebSocketDisconnect:
        print("[SERVER] ESP32 terputus (Disconnect normal)")
    except Exception as e:
        print(f"[SERVER] Koneksi error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
    
