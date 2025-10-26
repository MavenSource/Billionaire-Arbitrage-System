"""
Lightweight Merkle Tree Implementation
A simple but effective Merkle tree for transaction bundle verification.
"""

import hashlib
from typing import List, Optional


class MerkleTools:
    """Simple Merkle tree implementation for transaction bundling."""
    
    def __init__(self, hash_type: str = "sha256"):
        """
        Initialize Merkle tree.
        
        Args:
            hash_type: Hash algorithm to use (default: sha256)
        """
        self.hash_type = hash_type
        self.leaves = []
        self.tree = []
        self.is_ready = False
        
    def _hash(self, data: str) -> str:
        """Hash data using specified algorithm."""
        if self.hash_type == "sha256":
            return hashlib.sha256(data.encode()).hexdigest()
        else:
            raise ValueError(f"Unsupported hash type: {self.hash_type}")
    
    def add_leaf(self, values: List[str], do_hash: bool = False):
        """
        Add leaves to the tree.
        
        Args:
            values: List of values to add as leaves
            do_hash: Whether to hash the values (True) or use as-is (False)
        """
        self.is_ready = False
        for value in values:
            if do_hash:
                self.leaves.append(self._hash(value))
            else:
                self.leaves.append(value)
    
    def make_tree(self):
        """Build the Merkle tree from leaves."""
        self.is_ready = False
        if not self.leaves:
            return
        
        self.tree = [self.leaves]
        
        # Build tree level by level
        while len(self.tree[-1]) > 1:
            level = []
            prev_level = self.tree[-1]
            
            # Process pairs
            for i in range(0, len(prev_level), 2):
                left = prev_level[i]
                # If odd number of nodes, duplicate the last one
                right = prev_level[i + 1] if i + 1 < len(prev_level) else left
                # Hash the concatenation
                combined = left + right
                level.append(self._hash(combined))
            
            self.tree.append(level)
        
        self.is_ready = True
    
    def get_merkle_root(self) -> Optional[str]:
        """
        Get the Merkle root of the tree.
        
        Returns:
            Merkle root hash as hex string, or None if tree not ready
        """
        if not self.is_ready or not self.tree:
            return None
        return self.tree[-1][0]
    
    def get_proof(self, index: int) -> List[dict]:
        """
        Get Merkle proof for a leaf at given index.
        
        Args:
            index: Index of the leaf to prove
            
        Returns:
            List of proof elements with position and hash
        """
        if not self.is_ready or index >= len(self.leaves):
            return []
        
        proof = []
        current_index = index
        
        # Traverse tree levels (except root)
        for level_idx in range(len(self.tree) - 1):
            level = self.tree[level_idx]
            
            # Determine sibling
            if current_index % 2 == 0:
                # Current node is left, sibling is right
                sibling_index = current_index + 1
                position = "right"
            else:
                # Current node is right, sibling is left
                sibling_index = current_index - 1
                position = "left"
            
            # Get sibling hash (or duplicate if at end)
            if sibling_index < len(level):
                sibling_hash = level[sibling_index]
            else:
                sibling_hash = level[current_index]
            
            proof.append({
                "position": position,
                "hash": sibling_hash
            })
            
            # Move to parent index
            current_index = current_index // 2
        
        return proof
    
    def validate_proof(self, proof: List[dict], target_hash: str, merkle_root: str) -> bool:
        """
        Validate a Merkle proof.
        
        Args:
            proof: Proof elements from get_proof()
            target_hash: Hash of the leaf being proven
            merkle_root: Expected root hash
            
        Returns:
            True if proof is valid, False otherwise
        """
        current_hash = target_hash
        
        for element in proof:
            if element["position"] == "left":
                combined = element["hash"] + current_hash
            else:
                combined = current_hash + element["hash"]
            current_hash = self._hash(combined)
        
        return current_hash == merkle_root


# Create module-level object for backwards compatibility
merkletools = type('merkletools', (), {'MerkleTools': MerkleTools})()
