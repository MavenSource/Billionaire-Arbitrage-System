"""
Advanced Opportunity Detection Module
Real-time detection and analysis of arbitrage opportunities across DEXs.
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
import logging
import time
from dataclasses import dataclass, field


@dataclass
class Pool:
    """Represents a liquidity pool."""
    dex: str
    address: str
    token0: str
    token1: str
    reserve0: Decimal
    reserve1: Decimal
    fee: Decimal = Decimal('0.003')
    liquidity: Decimal = Decimal('0')
    
    def get_price(self, token: str) -> Decimal:
        """Get price of token in terms of the other token."""
        if token == self.token0 and self.reserve1 > 0:
            return self.reserve1 / self.reserve0
        elif token == self.token1 and self.reserve0 > 0:
            return self.reserve0 / self.reserve1
        return Decimal('0')


@dataclass
class OpportunityMetrics:
    """Metrics for an arbitrage opportunity."""
    profit_usd: Decimal
    profit_percentage: Decimal
    confidence_score: Decimal
    execution_time_ms: int
    gas_estimate: int
    slippage_estimate: Decimal
    liquidity_depth: Decimal
    risk_level: str = "medium"


class OpportunityDetector:
    """Advanced opportunity detection with real-time analysis."""
    
    def __init__(self, web3=None, math_engine=None):
        self.web3 = web3
        self.math_engine = math_engine
        self.logger = logging.getLogger("OpportunityDetector")
        
        # Detection parameters
        self.min_profit_usd = Decimal('10')
        self.min_profit_percentage = Decimal('0.5')
        self.max_slippage = Decimal('2.0')
        
        # Tracking
        self.opportunities_found = 0
        self.opportunities_executed = 0
        self.last_scan_time = 0
        
    def detect_opportunities(self, pools: List[Pool]) -> List[Dict]:
        """
        Detect arbitrage opportunities from pool data.
        Returns list of opportunities with detailed metrics.
        """
        opportunities = []
        scan_start = time.time()
        
        try:
            # Compare pools pairwise for arbitrage
            for i, pool1 in enumerate(pools):
                for pool2 in pools[i+1:]:
                    # Check if pools share tokens
                    if self._pools_compatible(pool1, pool2):
                        opportunity = self._analyze_pair(pool1, pool2)
                        if opportunity:
                            opportunities.append(opportunity)
                            self.opportunities_found += 1
            
            # Sort by profit descending
            opportunities.sort(
                key=lambda x: x['metrics'].profit_usd, 
                reverse=True
            )
            
            scan_duration = (time.time() - scan_start) * 1000
            self.last_scan_time = scan_duration
            
            self.logger.info(
                f"🔍 Scan complete: {len(opportunities)} opportunities found "
                f"in {scan_duration:.2f}ms"
            )
            
        except Exception as e:
            self.logger.error(f"Detection error: {e}")
        
        return opportunities
    
    def _pools_compatible(self, pool1: Pool, pool2: Pool) -> bool:
        """Check if two pools can be used for arbitrage."""
        if pool1.dex == pool2.dex:
            return False
        
        # Check for common token pairs
        tokens1 = {pool1.token0, pool1.token1}
        tokens2 = {pool2.token0, pool2.token1}
        
        return len(tokens1 & tokens2) == 2  # Same token pair
    
    def _analyze_pair(self, pool1: Pool, pool2: Pool) -> Optional[Dict]:
        """Analyze a pair of pools for arbitrage opportunity."""
        try:
            if not self.math_engine:
                return None
            
            # Determine common tokens
            token_in = pool1.token0
            token_out = pool1.token1
            
            # Calculate reserves
            reserves1 = (pool1.reserve0, pool1.reserve1)
            reserves2 = (pool2.reserve0, pool2.reserve1)
            
            # Test with standard amount
            test_amount = Decimal('1000')
            
            # Calculate profit using math engine
            result = self.math_engine.calculate_arbitrage_profit(
                test_amount, reserves1, reserves2
            )
            
            if not result['is_profitable']:
                return None
            
            # Calculate metrics
            metrics = self._calculate_metrics(result, pool1, pool2)
            
            # Check thresholds
            if (metrics.profit_usd < self.min_profit_usd or
                metrics.profit_percentage < self.min_profit_percentage):
                return None
            
            opportunity = {
                'pool1': {
                    'dex': pool1.dex,
                    'address': pool1.address,
                    'token0': pool1.token0,
                    'token1': pool1.token1,
                },
                'pool2': {
                    'dex': pool2.dex,
                    'address': pool2.address,
                    'token0': pool2.token0,
                    'token1': pool2.token1,
                },
                'input_amount': test_amount,
                'expected_output': result['output_amount'],
                'profit': result['net_profit'],
                'metrics': metrics,
                'timestamp': time.time()
            }
            
            return opportunity
            
        except Exception as e:
            self.logger.error(f"Analysis error: {e}")
            return None
    
    def _calculate_metrics(self, result: Dict, pool1: Pool, 
                          pool2: Pool) -> OpportunityMetrics:
        """Calculate detailed metrics for an opportunity."""
        # Estimate gas (typical arbitrage transaction)
        gas_estimate = 300_000
        
        # Estimate slippage based on liquidity
        total_liquidity = pool1.liquidity + pool2.liquidity
        slippage = Decimal('1.0') / (Decimal('1') + total_liquidity / Decimal('100000'))
        
        # Calculate confidence score (0-100)
        confidence = self._calculate_confidence(result, pool1, pool2)
        
        # Determine risk level
        risk = self._assess_risk(result, slippage, total_liquidity)
        
        # Estimate execution time
        execution_time = 150  # ~150ms target
        
        metrics = OpportunityMetrics(
            profit_usd=result['net_profit'],
            profit_percentage=result['profit_percentage'],
            confidence_score=confidence,
            execution_time_ms=execution_time,
            gas_estimate=gas_estimate,
            slippage_estimate=slippage,
            liquidity_depth=total_liquidity,
            risk_level=risk
        )
        
        return metrics
    
    def _calculate_confidence(self, result: Dict, pool1: Pool, 
                             pool2: Pool) -> Decimal:
        """Calculate confidence score for an opportunity."""
        score = Decimal('50')  # Base score
        
        # Higher profit increases confidence
        if result['profit_percentage'] > 5:
            score += Decimal('20')
        elif result['profit_percentage'] > 2:
            score += Decimal('10')
        
        # Higher liquidity increases confidence
        total_liquidity = pool1.liquidity + pool2.liquidity
        if total_liquidity > 1_000_000:
            score += Decimal('20')
        elif total_liquidity > 100_000:
            score += Decimal('10')
        
        # Lower slippage increases confidence
        if pool1.reserve0 > 10_000 and pool1.reserve1 > 10_000:
            score += Decimal('10')
        
        return min(score, Decimal('100'))
    
    def _assess_risk(self, result: Dict, slippage: Decimal, 
                     liquidity: Decimal) -> str:
        """Assess risk level of opportunity."""
        if slippage > Decimal('2.0') or liquidity < 10_000:
            return "high"
        elif slippage > Decimal('1.0') or liquidity < 100_000:
            return "medium"
        else:
            return "low"
    
    def get_statistics(self) -> Dict:
        """Get detector statistics."""
        success_rate = (
            self.opportunities_executed / max(self.opportunities_found, 1) * 100
        )
        
        return {
            'opportunities_found': self.opportunities_found,
            'opportunities_executed': self.opportunities_executed,
            'success_rate': f"{success_rate:.1f}%",
            'last_scan_time_ms': self.last_scan_time
        }