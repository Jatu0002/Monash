#!/usr/bin/env python3
"""
Test suite for the shopping cart system to verify the fix.
"""

import unittest
from shopping_cart_fixed import Container, BuggyContainer, Item, LootCapacityError

class TestShoppingCart(unittest.TestCase):
    
    def test_buggy_version_matches_issue_2(self):
        """Test that the buggy version produces the wrong output mentioned in issue #2"""
        buggy_cart = BuggyContainer("Coles", empty_weight=43, capacity=0)
        expected_wrong_output = "A coles shopping cart (total weight: 30, empty weight: 1, capacity: 28/1000)"
        self.assertEqual(str(buggy_cart), expected_wrong_output)
    
    def test_fixed_version_matches_issue_3(self):
        """Test that the fixed version produces the correct output mentioned in issue #3"""
        fixed_cart = Container("Coles", empty_weight=43, capacity=0)
        expected_correct_output = "A coles shopping cart (total weight: 71, empty weight: 43, capacity: 0/0)"
        self.assertEqual(str(fixed_cart), expected_correct_output)
    
    def test_coles_cart_inherent_weight(self):
        """Test that Coles cart has inherent weight of 28"""
        cart = Container("Coles", empty_weight=43, capacity=0)
        # Total (71) - Empty (43) = Inherent weight (28)
        self.assertEqual(cart.inherent_weight, 28)
        self.assertEqual(cart.get_total_weight(), 71)
    
    def test_other_cart_no_inherent_weight(self):
        """Test that non-Coles carts don't have inherent weight"""
        cart = Container("Woolworths", empty_weight=10, capacity=100)
        self.assertEqual(cart.inherent_weight, 0)
        self.assertEqual(cart.get_total_weight(), 10)
    
    def test_capacity_handling(self):
        """Test that capacity constraints work properly"""
        cart = Container("TestCart", empty_weight=5, capacity=10)
        
        # Should be able to add items within capacity
        item1 = Item("Light item", 5)
        cart.add_item(item1)
        self.assertEqual(cart.get_used_capacity(), 5)
        
        # Should raise error when exceeding capacity
        item2 = Item("Heavy item", 6)
        with self.assertRaises(LootCapacityError):
            cart.add_item(item2)
    
    def test_item_weight_calculation(self):
        """Test that item weights are calculated correctly"""
        cart = Container("TestCart", empty_weight=10, capacity=100)
        
        item1 = Item("Item 1", 3)
        item2 = Item("Item 2", 7)
        
        cart.add_item(item1)
        cart.add_item(item2)
        
        self.assertEqual(cart.get_used_capacity(), 10)
        self.assertEqual(cart.get_total_weight(), 20)  # 10 (empty) + 10 (items)

if __name__ == '__main__':
    unittest.main()