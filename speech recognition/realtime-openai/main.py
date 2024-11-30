

import pyaudio 
import websockets
import asyncio
import base64
import json
from api_secrets import API_KEY_ASSEMBLYAI

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

async def send_receive():
    async with websockets.connect(
        URL,
        ping_timeout=20,
        ping_interval=5,
        extra_headers={"Authorization": API_KEY_ASSEMBLYAI}
    ) as _ws:
        session_begins = await _ws.recv()
        print("Session started:", session_begins)

        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": data})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print("Connection closed while sending:", e)
                    break
                except Exception as e:
                    print("Error sending data:", e)
                    break
                await asyncio.sleep(0.01)

        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(result_str)
                    prompt = result.get("text", "")
                    if prompt and result.get("message_type") == "FinalTranscript":
                        print("Me:", prompt)
                        # Process response here
                        print("Bot: This is my answer")  # Example response
                except websockets.exceptions.ConnectionClosedError as e:
                    print("Connection closed while receiving:", e)
                    break
                except Exception as e:
                    print("Error receiving data:", e)
                    break
                await asyncio.sleep(0.01)

        await asyncio.gather(send(), receive())

if __name__ == "__main__":
    try:
        asyncio.run(send_receive())
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
