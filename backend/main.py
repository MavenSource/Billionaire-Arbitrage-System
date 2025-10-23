"""
Billionaire Arbitrage System - Backend API
FastAPI application providing arbitrage detection and execution endpoints.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from decimal import Decimal
import logging
import os
import asyncio
from datetime import datetime

# Import modules
from modules.advanced_dex_mathematics import ArbitrageMathEngine, QuantumMathEngine
from modules.web3_contract_integration import Web3ContractManager
from modules.flashloan_integration_flow import FlashloanFirstArbitrageScanner
from modules.advanced_opportunity_detection import OpportunityDetector, Pool

try:
    from web3 import Web3
except ImportError:
    Web3 = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("BillionaireArbitrage")

# Initialize FastAPI app
app = FastAPI(
    title="Billionaire Arbitrage System API",
    description="Institutional-grade DeFi arbitrage and MEV platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
system_state = {
    'initialized': False,
    'web3_connected': False,
    'opportunities_found': 0,
    'trades_executed': 0,
    'total_profit': Decimal('0'),
    'last_scan': None
}

# Initialize components
math_engine = ArbitrageMathEngine()
quantum_engine = QuantumMathEngine()
detector = OpportunityDetector(math_engine=math_engine)

web3_manager = None
flashloan_scanner = None

# WebSocket connections
active_connections: List[WebSocket] = []


# Pydantic models
class HealthResponse(BaseModel):
    status: str
    web3_connected: bool
    opportunities_found: int
    trades_executed: int
    total_profit: str
    last_scan: Optional[str]
    timestamp: str


class PoolInfo(BaseModel):
    dex: str
    address: str
    token0: str
    token1: str
    reserve0: str
    reserve1: str
    liquidity: str


class TradeRequest(BaseModel):
    dex: str
    token_in: str
    token_out: str
    amount_in: str
    min_amount_out: str
    slippage: Optional[float] = 0.5


class TradeResponse(BaseModel):
    success: bool
    tx_hash: Optional[str] = None
    error: Optional[str] = None
    profit: Optional[str] = None


# Initialize Web3 on startup
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    global web3_manager, flashloan_scanner, system_state
    
    logger.info("🚀 Starting Billionaire Arbitrage System...")
    
    # Get configuration from environment
    rpc_url = os.getenv('RPC_URL', os.getenv('POLYGON_RPC_URL', 'https://polygon-rpc.com'))
    private_key = os.getenv('PRIVATE_KEY')
    
    if not Web3:
        logger.warning("⚠️  Web3 not installed. Run: pip install web3")
        system_state['initialized'] = False
        return
    
    try:
        # Initialize Web3
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        config = {
            'RPC_URL': rpc_url,
            'PRIVATE_KEY': private_key
        }
        
        # Initialize managers
        web3_manager = Web3ContractManager(web3, config)
        flashloan_scanner = FlashloanFirstArbitrageScanner(
            web3, web3_manager, math_engine
        )
        
        # Check connection
        if web3_manager.is_connected():
            system_state['web3_connected'] = True
            logger.info(f"✅ Connected to network (Chain ID: {web3.eth.chain_id})")
            
            if web3_manager.account:
                balance = web3_manager.get_balance()
                logger.info(f"💰 Account balance: {balance} MATIC")
        else:
            logger.warning("⚠️  Web3 not connected")
        
        system_state['initialized'] = True
        logger.info("✅ System initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {e}")
        system_state['initialized'] = False


# API Endpoints
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Get system health status."""
    return HealthResponse(
        status="healthy" if system_state['initialized'] else "degraded",
        web3_connected=system_state['web3_connected'],
        opportunities_found=system_state['opportunities_found'],
        trades_executed=system_state['trades_executed'],
        total_profit=str(system_state['total_profit']),
        last_scan=system_state['last_scan'],
        timestamp=datetime.now().isoformat()
    )


@app.get("/api/pools", response_model=List[PoolInfo])
async def get_pools():
    """Get list of active liquidity pools."""
    # Return mock pool data for demonstration
    # In production, this would fetch real on-chain data
    pools = [
        PoolInfo(
            dex="UniswapV3",
            address="0x45dda9cb7c25131df268515131f647d726f50608",
            token0="USDC",
            token1="WETH",
            reserve0="1500000",
            reserve1="750",
            liquidity="5000000"
        ),
        PoolInfo(
            dex="QuickSwap",
            address="0x6e7a5fafcec6bb1e78bae2a1f0b612012bf14827",
            token0="USDC",
            token1="WMATIC",
            reserve0="2000000",
            reserve1="1500000",
            liquidity="8000000"
        ),
        PoolInfo(
            dex="SushiSwap",
            address="0xcd353f79d9fade311fc3119b841e1f456b54e858",
            token0="WETH",
            token1="USDT",
            reserve0="500",
            reserve1="1000000",
            liquidity="3500000"
        )
    ]
    
    logger.info(f"📊 Returning {len(pools)} pools")
    return pools


@app.post("/api/trade", response_model=TradeResponse)
async def execute_trade(trade: TradeRequest):
    """Execute a trade or arbitrage opportunity."""
    if not system_state['initialized']:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    if not web3_manager:
        raise HTTPException(status_code=503, detail="Web3 not available")
    
    try:
        logger.info(f"🔄 Executing trade: {trade.token_in} -> {trade.token_out} on {trade.dex}")
        
        # In production, this would execute actual transaction
        # For now, return mock success
        tx_hash = "0x" + "a" * 64
        profit = "25.50"
        
        system_state['trades_executed'] += 1
        system_state['total_profit'] += Decimal(profit)
        
        logger.info(f"✅ Trade executed: {tx_hash}")
        
        return TradeResponse(
            success=True,
            tx_hash=tx_hash,
            profit=profit
        )
        
    except Exception as e:
        logger.error(f"❌ Trade failed: {e}")
        return TradeResponse(
            success=False,
            error=str(e)
        )


@app.get("/api/opportunities")
async def get_opportunities():
    """Get current arbitrage opportunities."""
    if not system_state['initialized']:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        # Create mock pools for demonstration
        pools = [
            Pool(
                dex="UniswapV3",
                address="0x45dda9cb7c25131df268515131f647d726f50608",
                token0="USDC",
                token1="WETH",
                reserve0=Decimal('1500000'),
                reserve1=Decimal('750'),
                liquidity=Decimal('5000000')
            ),
            Pool(
                dex="QuickSwap",
                address="0x6e7a5fafcec6bb1e78bae2a1f0b612012bf14827",
                token0="USDC",
                token1="WETH",
                reserve0=Decimal('1480000'),
                reserve1=Decimal('740'),
                liquidity=Decimal('4800000')
            )
        ]
        
        # Detect opportunities
        opportunities = detector.detect_opportunities(pools)
        
        system_state['opportunities_found'] += len(opportunities)
        system_state['last_scan'] = datetime.now().isoformat()
        
        # Convert to JSON-serializable format
        result = []
        for opp in opportunities:
            result.append({
                'pool1': opp['pool1'],
                'pool2': opp['pool2'],
                'input_amount': str(opp['input_amount']),
                'expected_output': str(opp['expected_output']),
                'profit': str(opp['profit']),
                'profit_percentage': str(opp['metrics'].profit_percentage),
                'confidence': str(opp['metrics'].confidence_score),
                'risk': opp['metrics'].risk_level,
                'timestamp': opp['timestamp']
            })
        
        logger.info(f"🎯 Found {len(result)} opportunities")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error finding opportunities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_statistics():
    """Get system statistics."""
    stats = {
        'system': {
            'initialized': system_state['initialized'],
            'web3_connected': system_state['web3_connected'],
            'uptime': 'N/A'  # Would track actual uptime
        },
        'trading': {
            'opportunities_found': system_state['opportunities_found'],
            'trades_executed': system_state['trades_executed'],
            'total_profit': str(system_state['total_profit']),
            'last_scan': system_state['last_scan']
        },
        'detector': detector.get_statistics() if detector else {}
    }
    
    return stats


@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for live data streaming."""
    await websocket.accept()
    active_connections.append(websocket)
    
    logger.info("📡 WebSocket client connected")
    
    try:
        while True:
            # Send live updates
            update = {
                'type': 'status',
                'data': {
                    'opportunities': system_state['opportunities_found'],
                    'trades': system_state['trades_executed'],
                    'profit': str(system_state['total_profit']),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            await websocket.send_json(update)
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("📡 WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Billionaire Arbitrage System API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }


if __name__ == '__main__':
    import uvicorn
    
    port = int(os.getenv('PORT', 8000))
    
    logger.info(f"🚀 Starting server on port {port}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )