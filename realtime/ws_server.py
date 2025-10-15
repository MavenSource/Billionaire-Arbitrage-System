# /realtime/ws_server.py
import asyncio
import websockets
import msgpack
import json
import time
from collections import deque

PORT = 8765
USE_MSGPACK = True
latency_log = deque(maxlen=100)

async def handler(websocket):
    async for message in websocket:
        recv_time = time.perf_counter()
        if USE_MSGPACK:
            try:
                payload = msgpack.unpackb(message, raw=False)
            except Exception as e:
                await websocket.send(msgpack.packb({"error": str(e)}))
                continue
        else:
            payload = json.loads(message)

        payload["server_recv_timestamp"] = recv_time
        payload["server_echo"] = True

        if USE_MSGPACK:
            await websocket.send(msgpack.packb(payload))
        else:
            await websocket.send(json.dumps(payload))

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"[WS Server] Listening on port {PORT} (MsgPack: {USE_MSGPACK})")
        await asyncio.Future()  # Keep server alive

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("WebSocket server terminated.")
