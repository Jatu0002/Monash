#!/usr/bin/env python3

from inventory import Container, Item

def test_specific_issue():
    """Test the specific issue mentioned in problems statement vs issue #3"""
    
    print("=== Testing Issue #2 vs Issue #3 ===")
    
    # Issue #2 (problem statement): wrong output 
    # "A coles shopping cart (total weight: 30, empty weight: 1, capacity: 28/1000)"
    
    # Issue #3: correct output should be
    # "A coles shopping cart (total weight: 71, empty weight: 43, capacity: 0/0)"
    
    print("Problem: Issue #2 shows wrong output with total weight: 30, empty weight: 1")
    print("Expected: Issue #3 shows correct output should be total weight: 71, empty weight: 43, capacity: 0/0")
    print()
    
    # The key difference I notice:
    # 1. Total weight should be 71, not 30
    # 2. Empty weight should be 43, not 1  
    # 3. Capacity should show 0/0, not 28/1000
    
    # This suggests the cart specification itself is wrong in issue #2
    
    print("Creating cart as shown in issue #2 (wrong):")
    wrong_cart = Container("coles shopping cart", 1, 1000)
    
    # Add items to get total weight of 30
    wrong_items = [Item("wrong_item", 29)]
    for item in wrong_items:
        wrong_cart.add_item(item)
    
    print(f"Wrong cart: {wrong_cart}")
    print()
    
    print("Creating cart as should be in issue #3 (correct):")
    # To get total weight 71 with empty weight 43, we need items weighing 28
    correct_cart = Container("coles shopping cart", 43, 28)  # empty_weight=43, capacity=28
    
    # Add items that total 28 weight to fill the cart exactly
    correct_items = [
        Item("correct_item1", 15),
        Item("correct_item2", 13)
    ]
    
    for item in correct_items:
        correct_cart.add_item(item)
    
    print(f"Correct cart: {correct_cart}")
    print()
    
    print("Analysis:")
    print("- The issue was that the cart had wrong empty_weight (1 instead of 43)")
    print("- The issue was that the cart had wrong capacity (1000 instead of 28)")
    print("- When filled to capacity, it should show 0/0 remaining capacity")

if __name__ == "__main__":
    test_specific_issue()