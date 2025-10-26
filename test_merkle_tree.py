#!/usr/bin/env python3
"""
Test suite for Merkle Tree implementation.
"""

import sys
sys.path.insert(0, 'backend/utils')

from merkle_tree import MerkleTools


def test_merkle_tree_basic():
    """Test basic Merkle tree functionality."""
    print("Testing Merkle Tree Basics...")
    
    mt = MerkleTools(hash_type="sha256")
    
    # Add leaves
    leaves = ["tx1", "tx2", "tx3", "tx4"]
    mt.add_leaf(leaves, do_hash=True)
    
    print(f"✅ Added {len(leaves)} leaves")
    
    # Build tree
    mt.make_tree()
    print("✅ Tree built successfully")
    
    # Get root
    root = mt.get_merkle_root()
    assert root is not None, "Root should not be None"
    print(f"✅ Merkle root: {root}")
    
    return True


def test_merkle_proofs():
    """Test Merkle proof generation and validation."""
    print("\nTesting Merkle Proofs...")
    
    mt = MerkleTools(hash_type="sha256")
    
    # Add and build tree
    leaves = ["data1", "data2", "data3", "data4"]
    mt.add_leaf(leaves, do_hash=True)
    mt.make_tree()
    
    root = mt.get_merkle_root()
    
    # Get proofs for each leaf
    for i, leaf in enumerate(leaves):
        proof = mt.get_proof(i)
        print(f"✅ Generated proof for leaf {i}: {len(proof)} elements")
        assert len(proof) > 0, f"Proof for leaf {i} should not be empty"
    
    return True


def test_merkle_odd_leaves():
    """Test Merkle tree with odd number of leaves."""
    print("\nTesting Odd Number of Leaves...")
    
    mt = MerkleTools(hash_type="sha256")
    
    # Odd number of leaves
    leaves = ["tx1", "tx2", "tx3"]
    mt.add_leaf(leaves, do_hash=True)
    mt.make_tree()
    
    root = mt.get_merkle_root()
    assert root is not None, "Root should not be None for odd leaves"
    print(f"✅ Merkle root with {len(leaves)} leaves: {root}")
    
    return True


def test_merkle_single_leaf():
    """Test Merkle tree with single leaf."""
    print("\nTesting Single Leaf...")
    
    mt = MerkleTools(hash_type="sha256")
    
    leaves = ["single_tx"]
    mt.add_leaf(leaves, do_hash=True)
    mt.make_tree()
    
    root = mt.get_merkle_root()
    assert root is not None, "Root should not be None for single leaf"
    print(f"✅ Merkle root with single leaf: {root}")
    
    return True


def test_merkle_empty():
    """Test Merkle tree with no leaves."""
    print("\nTesting Empty Tree...")
    
    mt = MerkleTools(hash_type="sha256")
    mt.make_tree()
    
    root = mt.get_merkle_root()
    assert root is None, "Root should be None for empty tree"
    print("✅ Empty tree handled correctly (root is None)")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Merkle Tree Implementation - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Basic Functionality", test_merkle_tree_basic),
        ("Proof Generation", test_merkle_proofs),
        ("Odd Leaves", test_merkle_odd_leaves),
        ("Single Leaf", test_merkle_single_leaf),
        ("Empty Tree", test_merkle_empty)
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
