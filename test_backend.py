#!/usr/bin/env python3
"""
Simple test script to validate backend functionality.
"""

import sys
sys.path.insert(0, 'backend/modules')

from decimal import Decimal
from advanced_dex_mathematics import ArbitrageMathEngine, QuantumMathEngine
from advanced_opportunity_detection import OpportunityDetector, Pool

def test_math_engine():
    print("Testing Math Engine...")
    engine = ArbitrageMathEngine()
    
    # Test output amount calculation
    result = engine.calculate_output_amount(
        Decimal('1000'),
        Decimal('100000'),
        Decimal('50000')
    )
    print(f"✅ Output amount calculation: {result}")
    
    # Test arbitrage profit calculation
    profit = engine.calculate_arbitrage_profit(
        Decimal('1000'),
        (Decimal('100000'), Decimal('50000')),
        (Decimal('95000'), Decimal('52000'))
    )
    print(f"✅ Arbitrage profit: ${profit['net_profit']}")
    print(f"   Profit percentage: {profit['profit_percentage']}%")
    
    return True

def test_opportunity_detector():
    print("\nTesting Opportunity Detector...")
    math_engine = ArbitrageMathEngine()
    detector = OpportunityDetector(math_engine=math_engine)
    
    # Create test pools
    pools = [
        Pool(
            dex="UniswapV3",
            address="0x1234567890",
            token0="USDC",
            token1="WETH",
            reserve0=Decimal('1500000'),
            reserve1=Decimal('750'),
            liquidity=Decimal('5000000')
        ),
        Pool(
            dex="QuickSwap",
            address="0xabcdefghij",
            token0="USDC",
            token1="WETH",
            reserve0=Decimal('1480000'),
            reserve1=Decimal('740'),
            liquidity=Decimal('4800000')
        )
    ]
    
    opportunities = detector.detect_opportunities(pools)
    print(f"✅ Found {len(opportunities)} opportunities")
    
    # Get statistics
    stats = detector.get_statistics()
    print(f"✅ Detector stats: {stats}")
    
    return True

def main():
    print("=" * 60)
    print("Billionaire Arbitrage System - Backend Test")
    print("=" * 60)
    
    try:
        test_math_engine()
        test_opportunity_detector()
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed successfully!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
