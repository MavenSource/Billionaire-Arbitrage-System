"""
Advanced DEX Mathematics Module
Provides mathematical calculations for arbitrage opportunities, price impact, and slippage.
"""

from decimal import Decimal
from typing import Dict, List, Optional, Tuple
import math


class ArbitrageMathEngine:
    """Core mathematics engine for arbitrage calculations."""
    
    def __init__(self):
        self.min_profit_threshold = Decimal('0.001')  # 0.1% minimum profit
        
    def calculate_price_impact(self, amount_in: Decimal, reserve_in: Decimal, 
                               reserve_out: Decimal) -> Decimal:
        """Calculate price impact for a swap using constant product formula."""
        if reserve_in <= 0 or reserve_out <= 0:
            return Decimal('0')
        
        # x * y = k formula
        k = reserve_in * reserve_out
        new_reserve_in = reserve_in + amount_in
        new_reserve_out = k / new_reserve_in
        amount_out = reserve_out - new_reserve_out
        
        # Price impact as percentage
        expected_price = amount_in / (reserve_out / reserve_in)
        actual_price = amount_in / amount_out if amount_out > 0 else Decimal('0')
        
        if expected_price > 0:
            impact = abs(actual_price - expected_price) / expected_price * 100
            return impact
        return Decimal('0')
    
    def calculate_output_amount(self, amount_in: Decimal, reserve_in: Decimal,
                                reserve_out: Decimal, fee: Decimal = Decimal('0.003')) -> Decimal:
        """Calculate output amount for a swap with fees."""
        if reserve_in <= 0 or reserve_out <= 0 or amount_in <= 0:
            return Decimal('0')
        
        # Apply fee (e.g., 0.3% = 0.003)
        amount_in_with_fee = amount_in * (Decimal('1') - fee)
        
        # Constant product formula: (x + Δx) * (y - Δy) = x * y
        numerator = amount_in_with_fee * reserve_out
        denominator = reserve_in + amount_in_with_fee
        
        if denominator > 0:
            return numerator / denominator
        return Decimal('0')
    
    def calculate_arbitrage_profit(self, amount_in: Decimal, 
                                   dex1_reserves: Tuple[Decimal, Decimal],
                                   dex2_reserves: Tuple[Decimal, Decimal],
                                   gas_cost: Decimal = Decimal('0')) -> Dict:
        """
        Calculate potential arbitrage profit between two DEXs.
        Returns dict with profit, percentage, and execution path.
        """
        # Buy on DEX1
        amount_out_dex1 = self.calculate_output_amount(
            amount_in, dex1_reserves[0], dex1_reserves[1]
        )
        
        # Sell on DEX2
        amount_out_dex2 = self.calculate_output_amount(
            amount_out_dex1, dex2_reserves[1], dex2_reserves[0]
        )
        
        # Calculate profit
        gross_profit = amount_out_dex2 - amount_in
        net_profit = gross_profit - gas_cost
        profit_percentage = (net_profit / amount_in * 100) if amount_in > 0 else Decimal('0')
        
        is_profitable = net_profit > self.min_profit_threshold * amount_in
        
        return {
            'input_amount': amount_in,
            'intermediate_amount': amount_out_dex1,
            'output_amount': amount_out_dex2,
            'gross_profit': gross_profit,
            'net_profit': net_profit,
            'profit_percentage': profit_percentage,
            'gas_cost': gas_cost,
            'is_profitable': is_profitable
        }
    
    def optimize_input_amount(self, dex1_reserves: Tuple[Decimal, Decimal],
                              dex2_reserves: Tuple[Decimal, Decimal],
                              max_input: Decimal) -> Decimal:
        """
        Find optimal input amount for maximum profit using binary search.
        """
        low = Decimal('0.001')  # Minimum trade size
        high = max_input
        best_amount = low
        best_profit = Decimal('-inf')
        
        # Binary search for optimal amount
        iterations = 20
        for _ in range(iterations):
            mid = (low + high) / 2
            
            result = self.calculate_arbitrage_profit(mid, dex1_reserves, dex2_reserves)
            
            if result['net_profit'] > best_profit:
                best_profit = result['net_profit']
                best_amount = mid
            
            # Check if increasing amount increases profit
            test_higher = self.calculate_arbitrage_profit(
                mid * Decimal('1.1'), dex1_reserves, dex2_reserves
            )
            
            if test_higher['net_profit'] > result['net_profit']:
                low = mid
            else:
                high = mid
        
        return best_amount


class QuantumMathEngine:
    """Advanced mathematical calculations for quantum-inspired optimization."""
    
    def __init__(self):
        self.convergence_threshold = 1e-6
    
    def calculate_optimal_route(self, pools: List[Dict], 
                                amount_in: Decimal) -> List[Dict]:
        """
        Calculate optimal multi-hop route through multiple pools.
        Uses dynamic programming approach.
        """
        if not pools:
            return []
        
        # Simple greedy approach for multi-hop optimization
        # In production, this would use more sophisticated algorithms
        routes = []
        
        for i, pool in enumerate(pools):
            route_profit = self._calculate_route_profit(pool, amount_in)
            routes.append({
                'pool': pool,
                'profit': route_profit,
                'index': i
            })
        
        # Sort by profit descending
        routes.sort(key=lambda x: x['profit'], reverse=True)
        
        return routes[:5]  # Return top 5 routes
    
    def _calculate_route_profit(self, pool: Dict, amount: Decimal) -> Decimal:
        """Calculate expected profit for a route through a pool."""
        # Simplified calculation - in production would be more complex
        reserve_ratio = pool.get('reserve0', 1) / max(pool.get('reserve1', 1), 1)
        estimated_profit = amount * Decimal(str(reserve_ratio)) * Decimal('0.001')
        return estimated_profit
    
    def calculate_slippage_tolerance(self, volatility: float, 
                                     liquidity: Decimal) -> Decimal:
        """Calculate dynamic slippage tolerance based on market conditions."""
        base_slippage = Decimal('0.005')  # 0.5% base
        
        # Increase slippage for high volatility
        volatility_factor = Decimal(str(min(volatility * 2, 1.0)))
        
        # Decrease slippage for high liquidity
        liquidity_factor = Decimal('1') / (Decimal('1') + liquidity / Decimal('1000000'))
        
        dynamic_slippage = base_slippage * (Decimal('1') + volatility_factor) * liquidity_factor
        
        # Cap between 0.1% and 5%
        return max(min(dynamic_slippage, Decimal('0.05')), Decimal('0.001'))