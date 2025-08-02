#!/usr/bin/env python3
"""Tests for the shopping cart implementation."""

import unittest
from shopping_cart import ColesShoppingCart


class TestColesShoppingCart(unittest.TestCase):
    """Test cases for ColesShoppingCart class."""
    
    def test_empty_cart_string_representation(self):
        """Test string representation of an empty cart."""
        cart = ColesShoppingCart(empty_weight=43, max_capacity=0)
        expected = "A coles shopping cart (total weight: 43, empty weight: 43, capacity: 0/0)"
        self.assertEqual(str(cart), expected)
    
    def test_cart_with_items_string_representation(self):
        """Test string representation of cart with items - matches problem statement."""
        cart = ColesShoppingCart(empty_weight=43, max_capacity=0)
        cart.add_item("groceries", 28)  # Total weight becomes 71
        expected = "A coles shopping cart (total weight: 71, empty weight: 43, capacity: 0/0)"
        self.assertEqual(str(cart), expected)
    
    def test_cart_properties(self):
        """Test cart properties are calculated correctly."""
        cart = ColesShoppingCart(empty_weight=43, max_capacity=10)
        
        # Test initial state
        self.assertEqual(cart.empty_weight, 43)
        self.assertEqual(cart.max_capacity, 10)
        self.assertEqual(cart.total_weight, 43)
        
        # Test after adding items
        cart.add_item("item1", 15)
        cart.add_item("item2", 13)
        self.assertEqual(cart.total_weight, 71)  # 43 + 15 + 13
        self.assertEqual(len(cart.items), 2)


if __name__ == "__main__":
    unittest.main()