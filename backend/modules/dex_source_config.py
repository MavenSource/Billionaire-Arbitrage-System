"""
DEX Source Configuration Module
Provides comprehensive configuration for 30+ DEX sources across multiple chains.
Enables comparison of 15-25+ sources per scan cycle for enhanced arbitrage precision.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class ChainType(Enum):
    """Supported blockchain networks"""
    POLYGON = "polygon"
    ETHEREUM = "ethereum"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BSC = "bsc"

@dataclass
class DEXSource:
    """Configuration for a single DEX source"""
    name: str
    identifier: str
    chain: ChainType
    enabled: bool = True
    priority: int = 1  # Higher priority = scanned first
    router_address: Optional[str] = None
    factory_address: Optional[str] = None
    supports_flashloan: bool = False
    average_latency_ms: float = 100.0
    
class DEXSourceManager:
    """
    Manages DEX sources for multi-source arbitrage scanning.
    Supports 30+ DEX sources with configurable enable/disable per source.
    """
    
    def __init__(self):
        self.sources = self._initialize_sources()
        self.active_sources_count = 0
        self._update_active_count()
    
    def _initialize_sources(self) -> Dict[str, DEXSource]:
        """Initialize comprehensive list of 30+ DEX sources"""
        sources = {}
        
        # Polygon DEX Sources (Primary)
        polygon_dexs = [
            DEXSource("Uniswap V3", "uniswap_v3", ChainType.POLYGON, True, 10, 
                     "0xE592427A0AEce92De3Edee1F18E0157C05861564", supports_flashloan=False),
            DEXSource("QuickSwap", "quickswap", ChainType.POLYGON, True, 9,
                     "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff", supports_flashloan=False),
            DEXSource("SushiSwap", "sushiswap", ChainType.POLYGON, True, 9,
                     "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506", supports_flashloan=False),
            DEXSource("Balancer V2", "balancer_v2", ChainType.POLYGON, True, 10,
                     "0xBA12222222228d8Ba445958a75a0704d566BF2C8", supports_flashloan=True),
            DEXSource("Curve Finance", "curve", ChainType.POLYGON, True, 9,
                     supports_flashloan=False),
            DEXSource("DODO", "dodo", ChainType.POLYGON, True, 8,
                     supports_flashloan=True),
            DEXSource("1inch", "oneinch", ChainType.POLYGON, True, 8),
            DEXSource("Kyber Network", "kyber", ChainType.POLYGON, True, 7),
            DEXSource("Dfyn", "dfyn", ChainType.POLYGON, True, 7),
            DEXSource("ApeSwap", "apeswap", ChainType.POLYGON, True, 7),
            DEXSource("PolyDEX", "polydex", ChainType.POLYGON, True, 6),
            DEXSource("WaultSwap", "waultswap", ChainType.POLYGON, True, 6),
            DEXSource("Firebird Finance", "firebird", ChainType.POLYGON, True, 6),
            DEXSource("Jetswap", "jetswap", ChainType.POLYGON, True, 5),
            DEXSource("Polycat Finance", "polycat", ChainType.POLYGON, True, 5),
            DEXSource("PolyCrystal", "polycrystal", ChainType.POLYGON, True, 5),
            DEXSource("DinoSwap", "dinoswap", ChainType.POLYGON, True, 5),
            DEXSource("Gravity Finance", "gravity", ChainType.POLYGON, True, 5),
            DEXSource("Elk Finance", "elk", ChainType.POLYGON, True, 4),
            DEXSource("ComethSwap", "comethswap", ChainType.POLYGON, True, 4),
        ]
        
        # Ethereum DEX Sources
        ethereum_dexs = [
            DEXSource("Uniswap V3 (ETH)", "uniswap_v3_eth", ChainType.ETHEREUM, True, 10,
                     "0xE592427A0AEce92De3Edee1F18E0157C05861564", supports_flashloan=False),
            DEXSource("Uniswap V2 (ETH)", "uniswap_v2_eth", ChainType.ETHEREUM, True, 9,
                     "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", supports_flashloan=False),
            DEXSource("SushiSwap (ETH)", "sushiswap_eth", ChainType.ETHEREUM, True, 9,
                     "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F", supports_flashloan=False),
            DEXSource("Balancer V2 (ETH)", "balancer_v2_eth", ChainType.ETHEREUM, True, 10,
                     "0xBA12222222228d8Ba445958a75a0704d566BF2C8", supports_flashloan=True),
            DEXSource("Curve (ETH)", "curve_eth", ChainType.ETHEREUM, True, 9,
                     supports_flashloan=False),
            DEXSource("DODO (ETH)", "dodo_eth", ChainType.ETHEREUM, True, 8,
                     supports_flashloan=True),
            DEXSource("1inch (ETH)", "oneinch_eth", ChainType.ETHEREUM, True, 8),
            DEXSource("Bancor V3", "bancor_v3", ChainType.ETHEREUM, True, 7),
            DEXSource("Kyber (ETH)", "kyber_eth", ChainType.ETHEREUM, True, 7),
            DEXSource("Shibaswap", "shibaswap", ChainType.ETHEREUM, True, 6),
        ]
        
        # Additional Cross-Chain DEXs
        crosschain_dexs = [
            DEXSource("PancakeSwap V3", "pancake_v3", ChainType.BSC, True, 8),
            DEXSource("Camelot DEX", "camelot", ChainType.ARBITRUM, True, 7),
            DEXSource("Velodrome", "velodrome", ChainType.OPTIMISM, True, 7),
            DEXSource("TraderJoe", "traderjoe", ChainType.ARBITRUM, True, 6),
            DEXSource("Zyberswap", "zyberswap", ChainType.ARBITRUM, True, 6),
        ]
        
        # Combine all sources
        all_dexs = polygon_dexs + ethereum_dexs + crosschain_dexs
        
        for dex in all_dexs:
            sources[dex.identifier] = dex
        
        return sources
    
    def _update_active_count(self):
        """Update count of active sources"""
        self.active_sources_count = sum(1 for source in self.sources.values() if source.enabled)
    
    def get_enabled_sources(self, chain: Optional[ChainType] = None, 
                           min_priority: int = 0,
                           max_sources: Optional[int] = None) -> List[DEXSource]:
        """
        Get list of enabled DEX sources, optionally filtered by chain and priority.
        
        Args:
            chain: Filter by specific blockchain (None = all chains)
            min_priority: Minimum priority level (default 0 = all)
            max_sources: Maximum number of sources to return (None = all)
        
        Returns:
            List of enabled DEXSource objects, sorted by priority (highest first)
        """
        sources = [s for s in self.sources.values() if s.enabled]
        
        if chain:
            sources = [s for s in sources if s.chain == chain]
        
        if min_priority > 0:
            sources = [s for s in sources if s.priority >= min_priority]
        
        # Sort by priority (highest first)
        sources.sort(key=lambda x: x.priority, reverse=True)
        
        if max_sources:
            sources = sources[:max_sources]
        
        return sources
    
    def get_source_by_identifier(self, identifier: str) -> Optional[DEXSource]:
        """Get a specific DEX source by identifier"""
        return self.sources.get(identifier)
    
    def enable_source(self, identifier: str) -> bool:
        """Enable a specific DEX source"""
        source = self.sources.get(identifier)
        if source:
            source.enabled = True
            self._update_active_count()
            return True
        return False
    
    def disable_source(self, identifier: str) -> bool:
        """Disable a specific DEX source"""
        source = self.sources.get(identifier)
        if source:
            source.enabled = False
            self._update_active_count()
            return True
        return False
    
    def get_sources_with_flashloan(self) -> List[DEXSource]:
        """Get all enabled sources that support flashloans"""
        return [s for s in self.sources.values() if s.enabled and s.supports_flashloan]
    
    def get_statistics(self) -> Dict:
        """Get statistics about DEX sources"""
        enabled = [s for s in self.sources.values() if s.enabled]
        disabled = [s for s in self.sources.values() if not s.enabled]
        
        chains = {}
        for source in enabled:
            chain_name = source.chain.value
            chains[chain_name] = chains.get(chain_name, 0) + 1
        
        flashloan_count = sum(1 for s in enabled if s.supports_flashloan)
        
        return {
            "total_sources": len(self.sources),
            "enabled_sources": len(enabled),
            "disabled_sources": len(disabled),
            "sources_by_chain": chains,
            "flashloan_sources": flashloan_count,
            "average_latency_ms": sum(s.average_latency_ms for s in enabled) / len(enabled) if enabled else 0,
        }
    
    def set_bulk_enable(self, identifiers: List[str], enabled: bool = True):
        """Enable or disable multiple sources at once"""
        for identifier in identifiers:
            source = self.sources.get(identifier)
            if source:
                source.enabled = enabled
        self._update_active_count()
    
    def get_high_priority_sources(self, count: int = 20) -> List[DEXSource]:
        """
        Get top N highest priority enabled sources.
        Optimized for getting 15-25+ sources for scan cycles.
        
        Args:
            count: Number of sources to return (default 20)
        
        Returns:
            List of top priority enabled sources
        """
        return self.get_enabled_sources(max_sources=count)
    
    def get_polygon_sources(self, count: Optional[int] = None) -> List[DEXSource]:
        """Get Polygon-specific sources (primary chain for this system)"""
        return self.get_enabled_sources(chain=ChainType.POLYGON, max_sources=count)

# Global singleton instance
dex_source_manager = DEXSourceManager()

def get_dex_source_manager() -> DEXSourceManager:
    """Get global DEX source manager instance"""
    return dex_source_manager
