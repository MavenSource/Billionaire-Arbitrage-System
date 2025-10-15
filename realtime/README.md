# Realtime WebSocket Server

## Overview

This directory contains the ultra-low latency WebSocket server for the Billionaire-Arbitrage-System. The server is optimized for real-time data streaming and arbitrage opportunities.

## Features

- **Ultra-low roundtrip latency**: < 150ms target latency
- **Efficient binary serialization**: Uses msgpack for faster data transfer
- **AI/ML integration hooks**: Ready for AI/ML module integration
- **Scalable**: Designed for high-throughput arbitrage stream/data feeds

## Files

- `ws_server.py`: The main WebSocket server implementation
- `pm2.config.json`: PM2 process manager configuration

## Running the Server

### Manual Start

```bash
python3 realtime/ws_server.py
```

### Using PM2 (Recommended for Production)

```bash
# Install PM2 if not already installed
npm install -g pm2

# Start the WebSocket server
pm2 start realtime/pm2.config.json

# Check status
pm2 status

# View logs
pm2 logs ws-server

# Stop the server
pm2 stop ws-server

# Restart the server
pm2 restart ws-server
```

## Configuration

The server runs on port **8765** by default and uses **msgpack** for binary serialization.

You can modify these settings in `ws_server.py`:

```python
PORT = 8765          # Change the port
USE_MSGPACK = True   # Set to False to use JSON instead
```

## Integration

The WebSocket server is integrated with the existing Billionaire-Arbitrage-System architecture and provides the `/ws/live` endpoint mentioned in the main README.

### Client Connection

To connect to the WebSocket server:

```python
import asyncio
import websockets
import msgpack

async def connect():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Send data
        data = {"type": "request", "timestamp": time.time()}
        await websocket.send(msgpack.packb(data))
        
        # Receive response
        response = await websocket.recv()
        payload = msgpack.unpackb(response, raw=False)
        print(payload)

asyncio.run(connect())
```

## Performance

- Target latency: < 150ms roundtrip
- Supports concurrent connections
- Memory limit: 250MB per process (configurable in PM2)
- Auto-restart on failure

## Dependencies

Make sure you have the following Python packages installed:

```bash
pip install websockets msgpack
```

## Monitoring

When using PM2, you can monitor the server:

```bash
# Monitor in real-time
pm2 monit

# View detailed metrics
pm2 show ws-server
```
