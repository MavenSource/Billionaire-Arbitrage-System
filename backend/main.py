from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from modules import dex_sniper_billionaire, multi_tier_executor

app = FastAPI()

# Allow local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/api/pools")
def get_pools():
    # Example: fetch all pools from your arbitrage system
    return dex_sniper_billionaire.get_all_pools()

@app.get("/api/health")
def get_health():
    return dex_sniper_billionaire.get_health_status()

@app.post("/api/trade")
async def execute_trade(request: Request):
    params = await request.json()
    return multi_tier_executor.run_trade(params)

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Example: push live trade logs every few seconds
    while True:
        data = dex_sniper_billionaire.get_live_update()
        await websocket.send_json(data)