"""
Billionaire Arbitrage System - FastAPI Backend
Main entry point for the arbitrage system API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import sys
from decimal import Decimal
from dotenv import load_dotenv

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Billionaire Arbitrage System",
    description="DeFi arbitrage and MEV extraction platform",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TradeRequest(BaseModel):
    dex: str
    token_in: str
    token_out: str
    amount_in: int
    min_amount_out: int

class HealthResponse(BaseModel):
    status: str
    message: str
    rpc_configured: bool

class PoolData(BaseModel):
    pool_id: str
    dex: str
    token_a: str
    token_b: str
    liquidity: float

class MEVOpportunity(BaseModel):
    """MEV arbitrage opportunity model"""
    dex1: str
    dex2: str
    token_in: str
    token_out: str
    amount_in: str
    expected_profit: str
    profit_percentage: str
    is_profitable: bool
    gas_cost: str
    timestamp: float

class MEVStatusResponse(BaseModel):
    """MEV system status"""
    enabled: bool
    opportunities_detected: int
    bundles_submitted: int
    relays_configured: int

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Billionaire Arbitrage System API",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    rpc_url = os.getenv("RPC_URL", "")
    return HealthResponse(
        status="healthy",
        message="System is running",
        rpc_configured=bool(rpc_url and rpc_url != "https://polygon-rpc.com")
    )

@app.get("/api/pools", response_model=List[PoolData])
async def get_pools():
    """Fetch all DeFi pools"""
    # Return mock data for now - in production, this would fetch real pool data
    return [
        PoolData(
            pool_id="pool_001",
            dex="Uniswap V3",
            token_a="USDC",
            token_b="WETH",
            liquidity=1000000.0
        ),
        PoolData(
            pool_id="pool_002",
            dex="SushiSwap",
            token_a="USDC",
            token_b="WMATIC",
            liquidity=500000.0
        )
    ]

@app.post("/api/trade")
async def execute_trade(trade: TradeRequest):
    """Execute trade/arbitrage"""
    # Validate environment
    private_key = os.getenv("PRIVATE_KEY")
    rpc_url = os.getenv("RPC_URL")
    
    if not private_key or private_key == "your_private_key_here_without_0x_prefix":
        raise HTTPException(
            status_code=400,
            detail="Private key not configured. Please set PRIVATE_KEY in .env file"
        )
    
    if not rpc_url or rpc_url == "https://polygon-rpc.com":
        raise HTTPException(
            status_code=400,
            detail="RPC URL not configured. Please set RPC_URL in .env file"
        )
    
    # Return mock response - in production, this would execute real trades
    return {
        "status": "submitted",
        "tx_hash": "0x" + "0" * 64,
        "message": "Trade submitted successfully (mock mode)",
        "trade_details": trade.dict()
    }

@app.get("/api/mev/status", response_model=MEVStatusResponse)
async def mev_status():
    """Get MEV system status"""
    mev_enabled = os.getenv("MEV_ENABLED", "true").lower() == "true"
    
    # In production, these would be tracked in a state manager
    return MEVStatusResponse(
        enabled=mev_enabled,
        opportunities_detected=0,
        bundles_submitted=0,
        relays_configured=3  # Default number of relays
    )

@app.get("/api/mev/opportunities", response_model=List[MEVOpportunity])
async def get_mev_opportunities():
    """Get current MEV arbitrage opportunities"""
    # In production, this would fetch from the MEV detector
    try:
        from mev_stack import OpportunityDetector, MEVArbitrageMathEngine
        
        math_engine = MEVArbitrageMathEngine()
        detector = OpportunityDetector(math_engine)
        opportunities = detector.detect_live_opportunities()
        
        result = []
        for opp, reserves in opportunities:
            result.append(MEVOpportunity(
                dex1=opp.dex1,
                dex2=opp.dex2,
                token_in=opp.token_in,
                token_out=opp.token_out,
                amount_in=str(opp.amount_in),
                expected_profit=str(opp.expected_profit),
                profit_percentage=str(opp.profit_percentage),
                is_profitable=opp.is_profitable,
                gas_cost=str(opp.gas_cost),
                timestamp=opp.timestamp
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting opportunities: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
