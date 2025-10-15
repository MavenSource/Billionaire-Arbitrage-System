#!/usr/bin/env python3
"""
Example WebSocket client for testing the realtime WebSocket server.
Demonstrates how to connect and communicate with the server using msgpack.
"""

import asyncio
import websockets
import msgpack
import time
import json

# Server configuration
WS_SERVER_URI = "ws://localhost:8765"
USE_MSGPACK = True  # Set to False to use JSON instead

async def test_websocket_connection():
    """Test basic WebSocket connection and echo functionality."""
    print(f"Connecting to {WS_SERVER_URI}...")
    
    try:
        async with websockets.connect(WS_SERVER_URI) as websocket:
            print("✅ Connected to WebSocket server")
            
            # Prepare test message
            test_data = {
                "type": "test_message",
                "timestamp": time.time(),
                "data": "Hello from client",
                "sequence": 1
            }
            
            # Send message
            start_time = time.perf_counter()
            if USE_MSGPACK:
                await websocket.send(msgpack.packb(test_data))
                print(f"📤 Sent (msgpack): {test_data}")
            else:
                await websocket.send(json.dumps(test_data))
                print(f"📤 Sent (json): {test_data}")
            
            # Receive response
            response = await websocket.recv()
            end_time = time.perf_counter()
            
            if USE_MSGPACK:
                payload = msgpack.unpackb(response, raw=False)
            else:
                payload = json.loads(response)
            
            # Calculate latency
            latency_ms = (end_time - start_time) * 1000
            
            print(f"📥 Received: {payload}")
            print(f"⚡ Roundtrip latency: {latency_ms:.2f}ms")
            
            # Check if echo was successful
            if payload.get("server_echo") == True:
                print("✅ Server echo confirmed")
            
            return latency_ms
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def test_multiple_messages(count=10):
    """Test multiple messages to measure average latency."""
    print(f"\nTesting {count} messages...")
    latencies = []
    
    try:
        async with websockets.connect(WS_SERVER_URI) as websocket:
            for i in range(count):
                test_data = {
                    "type": "latency_test",
                    "timestamp": time.time(),
                    "sequence": i + 1
                }
                
                start_time = time.perf_counter()
                
                if USE_MSGPACK:
                    await websocket.send(msgpack.packb(test_data))
                else:
                    await websocket.send(json.dumps(test_data))
                
                response = await websocket.recv()
                end_time = time.perf_counter()
                
                latency_ms = (end_time - start_time) * 1000
                latencies.append(latency_ms)
                
                await asyncio.sleep(0.1)  # Small delay between messages
            
            # Calculate statistics
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            print(f"\n📊 Latency Statistics:")
            print(f"   Average: {avg_latency:.2f}ms")
            print(f"   Min: {min_latency:.2f}ms")
            print(f"   Max: {max_latency:.2f}ms")
            print(f"   Target: < 150ms")
            
            if avg_latency < 150:
                print("✅ Performance target met!")
            else:
                print("⚠️  Performance target not met")
                
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Run all tests."""
    print("=" * 60)
    print("WebSocket Server Test Client")
    print("=" * 60)
    print(f"Server: {WS_SERVER_URI}")
    print(f"Protocol: {'msgpack (binary)' if USE_MSGPACK else 'JSON (text)'}")
    print("=" * 60)
    
    # Test single message
    print("\n🧪 Test 1: Single Message Echo")
    print("-" * 60)
    await test_websocket_connection()
    
    # Test multiple messages
    print("\n🧪 Test 2: Multiple Messages (Latency Test)")
    print("-" * 60)
    await test_multiple_messages(10)
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
