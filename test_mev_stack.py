#!/usr/bin/env python3
"""
Test suite for MEV Stack Module.
Tests MEV arbitrage calculations, bundle building, and opportunity detection.
"""

import sys
sys.path.insert(0, 'backend/modules')

from decimal import Decimal
from mev_stack import (
    MEVArbitrageMathEngine,
    TxBundleBuilder,
    FlashloanArbitrageOrchestrator,
    OpportunityDetector,
    ArbitrageOpportunity
)
import time


def test_mev_math_engine():
    """Test MEV arbitrage math engine calculations."""
    print("Testing MEV Math Engine...")
    engine = MEVArbitrageMathEngine(min_profit_threshold=Decimal('0.001'))
    
    # Test output amount calculation
    amount_in = Decimal('1000')
    reserve_in = Decimal('500000')
    reserve_out = Decimal('500000')
    
    output = engine.calculate_output_amount(amount_in, reserve_in, reserve_out)
    print(f"✅ Output amount calculation: {output}")
    assert output > 0, "Output should be positive"
    assert output < amount_in, "Output should be less than input (due to fees)"
    
    # Test arbitrage profit calculation with profitable path
    dex_path = [
        (Decimal('500000'), Decimal('500000')),
        (Decimal('505000'), Decimal('495000'))
    ]
    gas_cost = Decimal('5')
    
    result = engine.calculate_arbitrage_profit(amount_in, dex_path, gas_cost)
    print(f"✅ Arbitrage calculation: Net profit = {result['net_profit']}")
    print(f"   Profit percentage: {result['profit_percentage']}%")
    print(f"   Is profitable: {result['is_profitable']}")
    
    assert 'input_amount' in result, "Result should contain input_amount"
    assert 'final_output' in result, "Result should contain final_output"
    assert 'gross_profit' in result, "Result should contain gross_profit"
    assert 'net_profit' in result, "Result should contain net_profit"
    assert 'profit_percentage' in result, "Result should contain profit_percentage"
    assert 'is_profitable' in result, "Result should contain is_profitable"
    
    # Test with empty path
    empty_result = engine.calculate_arbitrage_profit(amount_in, [], gas_cost)
    print(f"✅ Empty path handling: Net profit = {empty_result['net_profit']}")
    assert empty_result['net_profit'] < 0, "Empty path should show loss"
    assert not empty_result['is_profitable'], "Empty path should not be profitable"
    
    return True


def test_bundle_builder():
    """Test transaction bundle builder."""
    print("\nTesting Bundle Builder...")
    
    # Create mock Web3 instance (None is acceptable for this test)
    from unittest.mock import MagicMock
    web3_mock = MagicMock()
    
    # Initialize bundle builder without private key (for testing)
    relays = [
        "https://relay1.example.com",
        "https://relay2.example.com"
    ]
    builder = TxBundleBuilder(web3_mock, None, relays)
    
    # Test bundle creation
    signed_txs = [
        "0x1234567890abcdef",
        "0xfedcba0987654321"
    ]
    
    bundle = builder.build_bundle(signed_txs)
    print(f"✅ Bundle created with {len(signed_txs)} transactions")
    print(f"   Merkle root: {bundle['merkle_root']}")
    print(f"   Timestamp: {bundle['timestamp']}")
    
    assert 'txs' in bundle, "Bundle should contain txs"
    assert 'merkle_root' in bundle, "Bundle should contain merkle_root"
    assert 'proofs' in bundle, "Bundle should contain proofs"
    assert 'timestamp' in bundle, "Bundle should contain timestamp"
    assert bundle['txs'] == signed_txs, "Bundle txs should match input"
    assert len(bundle['proofs']) == len(signed_txs), "Should have proof for each tx"
    
    return True


def test_opportunity_detector():
    """Test opportunity detector."""
    print("\nTesting Opportunity Detector...")
    
    math_engine = MEVArbitrageMathEngine()
    detector = OpportunityDetector(math_engine)
    
    # Detect opportunities
    opportunities = detector.detect_live_opportunities()
    print(f"✅ Detected {len(opportunities)} opportunities")
    
    assert len(opportunities) > 0, "Should detect at least one opportunity"
    
    for i, (opp, reserves) in enumerate(opportunities):
        print(f"\n   Opportunity {i+1}:")
        print(f"   - DEX Route: {opp.dex1} -> {opp.dex2}")
        print(f"   - Tokens: {opp.token_in} -> {opp.token_out}")
        print(f"   - Amount: {opp.amount_in}")
        print(f"   - Expected Profit: {opp.expected_profit}")
        print(f"   - Profit %: {opp.profit_percentage}%")
        print(f"   - Reserves: {len(reserves)} pairs")
        
        assert isinstance(opp, ArbitrageOpportunity), "Should be ArbitrageOpportunity instance"
        assert opp.amount_in > 0, "Amount should be positive"
        assert len(reserves) > 0, "Should have reserve data"
    
    return True


def test_integration():
    """Test integration between components."""
    print("\nTesting Component Integration...")
    
    from unittest.mock import MagicMock
    
    # Setup components
    web3_mock = MagicMock()
    web3_mock.eth.block_number = 12345678
    
    math_engine = MEVArbitrageMathEngine()
    bundle_builder = TxBundleBuilder(web3_mock, None, ["https://relay.example.com"])
    orchestrator = FlashloanArbitrageOrchestrator(web3_mock, math_engine, bundle_builder)
    
    # Create test opportunity
    opportunity = ArbitrageOpportunity(
        dex1="uniswap",
        dex2="sushiswap",
        token_in="USDC",
        token_out="WETH",
        amount_in=Decimal('1000'),
        expected_profit=Decimal('15'),
        profit_percentage=Decimal('1.5'),
        is_profitable=True,
        gas_cost=Decimal('5'),
        timestamp=time.time()
    )
    
    reserves = [
        (Decimal('500000'), Decimal('250')),
        (Decimal('505000'), Decimal('248'))
    ]
    
    print(f"✅ Created test opportunity: {opportunity.token_in}/{opportunity.token_out}")
    print(f"   Expected profit: {opportunity.expected_profit}")
    
    # Note: We won't actually call process_opportunity in sync context as it's async
    # Just verify the components are compatible
    assert orchestrator.math_engine is not None, "Orchestrator should have math engine"
    assert orchestrator.bundle_builder is not None, "Orchestrator should have bundle builder"
    
    return True


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\nTesting Edge Cases...")
    
    engine = MEVArbitrageMathEngine()
    
    # Test with zero reserves
    output = engine.calculate_output_amount(
        Decimal('1000'),
        Decimal('0'),
        Decimal('500000')
    )
    assert output == Decimal('0'), "Should return 0 for zero reserves"
    print("✅ Zero reserves handled correctly")
    
    # Test with negative input (should be caught by conversion)
    output = engine.calculate_output_amount(
        Decimal('-1000'),
        Decimal('500000'),
        Decimal('500000')
    )
    assert output == Decimal('0'), "Should return 0 for negative input"
    print("✅ Negative input handled correctly")
    
    # Test with very small amounts
    output = engine.calculate_output_amount(
        Decimal('0.001'),
        Decimal('1000000'),
        Decimal('1000000')
    )
    assert output > 0, "Should handle small amounts"
    print(f"✅ Small amount handled: {output}")
    
    # Test profitability threshold
    result = engine.calculate_arbitrage_profit(
        Decimal('1000'),
        [(Decimal('1000000'), Decimal('1000000')), (Decimal('1000000'), Decimal('1000000'))],
        Decimal('0')
    )
    print(f"✅ Profitability check: {result['is_profitable']} (threshold: {engine.min_profit_threshold})")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("MEV Stack Module - Test Suite")
    print("=" * 60)
    
    tests = [
        ("MEV Math Engine", test_mev_math_engine),
        ("Bundle Builder", test_bundle_builder),
        ("Opportunity Detector", test_opportunity_detector),
        ("Integration", test_integration),
        ("Edge Cases", test_edge_cases)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("🎉 All tests passed successfully!")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
