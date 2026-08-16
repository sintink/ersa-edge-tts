import os
import asyncio
import websockets
import json
import edge_tts

PORT = int(os.environ.get("PORT", 8080))

async def text_to_speech(text, output_file="output.mp3"):
    communicate = edge_tts.Communicate(text, "id-ID-GadisNeural") # Suara wanita natural Indonesia
    await communicate.save(output_file)

async def handler(websocket, path):
    print("ESP32 Berhasil Terhubung!")
    try:
        async for message in websocket:
            data = json.loads(message)
            user_text = data.get("text", "")
            print(f"Menerima dari ESP32: {user_text}")

            # Untuk tes awal, AI menjawab otomatis berdasarkan ucapan kamu
            ai_response = f"Kamu bilang: {user_text}"
            
            # Ubah teks balasan jadi suara pakai Edge TTS
            await text_to_speech(ai_response)
            
            # Kirim balik ke ESP32
            await websocket.send(json.dumps({
                "type": "tts",
                "text": ai_response,
                "audio_url": "proses_audio" 
            }))
            
    except websockets.exceptions.ConnectionClosed:
        print("ESP32 Terputus")

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Server WebSocket aktif di port {PORT}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
    
