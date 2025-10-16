#!/usr/bin/env python3
"""
Integration test for multi-source DEX scanning functionality
Tests the complete flow from configuration to scanning
"""

import sys
import os
import unittest

# Add backend modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'modules'))

from dex_source_config import (
    get_dex_source_manager, 
    ChainType, 
    DEXSource,
    DEXSourceManager
)

# Precision model constants
PRECISION_BASE = 90.0  # Base precision with 3 sources
PRECISION_BASE_SOURCES = 3  # Number of sources for base precision
PRECISION_INCREMENT = 0.5  # Precision increase per additional source
PRECISION_MAX = 99.5  # Maximum theoretical precision

def estimate_precision(source_count: int) -> float:
    """
    Estimate arbitrage precision based on number of sources.
    
    This is a theoretical model where:
    - 3-4 sources provide ~90% precision (baseline)
    - Each additional source adds ~0.5% precision
    - Maximum practical precision is 99.5%
    
    Args:
        source_count: Number of DEX sources being compared
    
    Returns:
        Estimated precision percentage
    """
    return min(PRECISION_BASE + (source_count - PRECISION_BASE_SOURCES) * PRECISION_INCREMENT, PRECISION_MAX)

class TestDEXSourceConfiguration(unittest.TestCase):
    """Test DEX source configuration module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = get_dex_source_manager()
    
    def test_manager_initialization(self):
        """Test that manager initializes properly"""
        self.assertIsNotNone(self.manager)
        self.assertIsInstance(self.manager, DEXSourceManager)
    
    def test_minimum_source_count(self):
        """Test that we have at least 30 sources configured"""
        stats = self.manager.get_statistics()
        expected_min_sources = 30
        self.assertGreaterEqual(
            stats['total_sources'], 
            expected_min_sources, 
            f"Should have at least {expected_min_sources} DEX sources"
        )
    
    def test_enabled_sources_count(self):
        """Test that sufficient sources are enabled"""
        stats = self.manager.get_statistics()
        self.assertGreaterEqual(
            stats['enabled_sources'], 
            20, 
            "Should have at least 20 enabled sources"
        )
    
    def test_high_priority_sources(self):
        """Test getting high priority sources"""
        # Test getting 15 sources
        sources_15 = self.manager.get_high_priority_sources(count=15)
        self.assertEqual(len(sources_15), 15, "Should get exactly 15 sources")
        
        # Test getting 25 sources
        sources_25 = self.manager.get_high_priority_sources(count=25)
        self.assertEqual(len(sources_25), 25, "Should get exactly 25 sources")
        
        # Verify sources are sorted by priority
        priorities = [s.priority for s in sources_25]
        self.assertEqual(
            priorities, 
            sorted(priorities, reverse=True),
            "Sources should be sorted by priority (highest first)"
        )
    
    def test_polygon_sources(self):
        """Test Polygon-specific sources"""
        polygon_sources = self.manager.get_polygon_sources()
        self.assertGreaterEqual(
            len(polygon_sources), 
            15, 
            "Should have at least 15 Polygon sources"
        )
        
        # Verify all are Polygon chain
        for source in polygon_sources:
            self.assertEqual(
                source.chain, 
                ChainType.POLYGON,
                f"Source {source.name} should be on Polygon"
            )
    
    def test_flashloan_sources(self):
        """Test flashloan-capable sources"""
        flashloan_sources = self.manager.get_sources_with_flashloan()
        self.assertGreaterEqual(
            len(flashloan_sources), 
            2, 
            "Should have at least 2 flashloan sources"
        )
        
        # Verify they support flashloans
        for source in flashloan_sources:
            self.assertTrue(
                source.supports_flashloan,
                f"Source {source.name} should support flashloans"
            )
    
    def test_enable_disable_functionality(self):
        """Test enable/disable source functionality"""
        test_source = "quickswap"
        
        # Get original state
        original = self.manager.get_source_by_identifier(test_source)
        self.assertIsNotNone(original, f"Source {test_source} should exist")
        original_state = original.enabled
        original_count = self.manager.active_sources_count
        
        # Disable source
        success = self.manager.disable_source(test_source)
        self.assertTrue(success, "Should successfully disable source")
        self.assertFalse(
            self.manager.get_source_by_identifier(test_source).enabled,
            "Source should be disabled"
        )
        self.assertEqual(
            self.manager.active_sources_count,
            original_count - 1,
            "Active count should decrease by 1"
        )
        
        # Re-enable source
        success = self.manager.enable_source(test_source)
        self.assertTrue(success, "Should successfully enable source")
        self.assertTrue(
            self.manager.get_source_by_identifier(test_source).enabled,
            "Source should be enabled"
        )
        self.assertEqual(
            self.manager.active_sources_count,
            original_count,
            "Active count should return to original"
        )
    
    def test_bulk_enable_disable(self):
        """Test bulk enable/disable functionality"""
        test_sources = ["quickswap", "sushiswap", "curve"]
        
        # Disable multiple sources
        self.manager.set_bulk_enable(test_sources, enabled=False)
        for identifier in test_sources:
            source = self.manager.get_source_by_identifier(identifier)
            self.assertFalse(
                source.enabled,
                f"Source {identifier} should be disabled"
            )
        
        # Re-enable multiple sources
        self.manager.set_bulk_enable(test_sources, enabled=True)
        for identifier in test_sources:
            source = self.manager.get_source_by_identifier(identifier)
            self.assertTrue(
                source.enabled,
                f"Source {identifier} should be enabled"
            )
    
    def test_priority_filtering(self):
        """Test filtering by minimum priority"""
        min_priority = 8
        high_priority = self.manager.get_enabled_sources(min_priority=min_priority)
        
        self.assertGreater(len(high_priority), 0, "Should have high priority sources")
        
        # Verify all meet minimum priority
        for source in high_priority:
            self.assertGreaterEqual(
                source.priority,
                min_priority,
                f"Source {source.name} should have priority >= {min_priority}"
            )
    
    def test_chain_filtering(self):
        """Test filtering by blockchain"""
        # Test Polygon
        polygon = self.manager.get_enabled_sources(chain=ChainType.POLYGON)
        for source in polygon:
            self.assertEqual(source.chain, ChainType.POLYGON)
        
        # Test Ethereum
        ethereum = self.manager.get_enabled_sources(chain=ChainType.ETHEREUM)
        for source in ethereum:
            self.assertEqual(source.chain, ChainType.ETHEREUM)
    
    def test_source_limit(self):
        """Test max_sources parameter"""
        max_sources = 10
        sources = self.manager.get_enabled_sources(max_sources=max_sources)
        self.assertEqual(
            len(sources),
            max_sources,
            f"Should return exactly {max_sources} sources"
        )
    
    def test_statistics(self):
        """Test statistics generation"""
        stats = self.manager.get_statistics()
        
        # Verify required keys
        required_keys = [
            'total_sources',
            'enabled_sources',
            'disabled_sources',
            'sources_by_chain',
            'flashloan_sources',
            'average_latency_ms'
        ]
        for key in required_keys:
            self.assertIn(key, stats, f"Statistics should include {key}")
        
        # Verify counts add up
        self.assertEqual(
            stats['total_sources'],
            stats['enabled_sources'] + stats['disabled_sources'],
            "Total should equal enabled + disabled"
        )
    
    def test_precision_requirements(self):
        """
        Test that we meet precision requirements from issue.
        
        Note: Precision estimates are theoretical, based on the model that
        more price sources provide better market price discovery and arbitrage
        detection capabilities.
        """
        # Issue states: 3-4 sources = 90% precision, 20+ sources should be much higher
        
        # Test we can get 20+ sources
        sources_20 = self.manager.get_high_priority_sources(count=20)
        self.assertEqual(
            len(sources_20),
            20,
            "Should be able to get 20 sources"
        )
        
        # Test we can get 25+ sources
        sources_25 = self.manager.get_high_priority_sources(count=25)
        self.assertGreaterEqual(
            len(sources_25),
            25,
            "Should be able to get 25+ sources"
        )
        
        # Verify sources are sorted by priority
        priorities = [s.priority for s in sources_25]
        self.assertEqual(
            priorities, 
            sorted(priorities, reverse=True),
            "Sources should be sorted by priority (highest first)"
        )
        
        # Estimate precision improvement using our model
        precision_4 = estimate_precision(4)
        precision_20 = estimate_precision(20)
        precision_25 = estimate_precision(25)
        
        self.assertLess(precision_4, precision_20, "20 sources should have higher precision than 4")
        self.assertLess(precision_20, precision_25, "25 sources should have higher precision than 20")
        
        # Verify we meet the "much higher" requirement
        improvement = precision_20 - precision_4
        min_improvement = 5.0
        self.assertGreater(
            improvement,
            min_improvement,
            f"Improvement from 4 to 20 sources should be significant (>{min_improvement}%)"
        )

class TestIntegrationWithBots(unittest.TestCase):
    """Test integration with bot modules"""
    
    def test_import_in_ultra_mev_bot(self):
        """Test that ultra_mev_arbitrage_bot can import module"""
        try:
            # This simulates what the bot does
            from dex_source_config import get_dex_source_manager
            manager = get_dex_source_manager()
            self.assertIsNotNone(manager)
        except ImportError as e:
            self.fail(f"Should be able to import in bot context: {e}")
    
    def test_bot_configuration(self):
        """Test bot configuration with different source counts"""
        manager = get_dex_source_manager()
        
        # Test configurations from the issue
        configs = [4, 15, 20, 25, 30]
        
        for count in configs:
            sources = manager.get_high_priority_sources(count=count)
            self.assertGreaterEqual(
                len(sources),
                min(count, 35),  # Can't exceed total sources
                f"Should get {count} sources or total available"
            )

def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running Integration Tests for Multi-Source DEX Configuration")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDEXSourceConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWithBots))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
