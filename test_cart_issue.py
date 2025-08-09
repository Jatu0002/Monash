#!/usr/bin/env python3

from inventory import Container, Item

def test_shopping_cart_issue():
    """Test to reproduce the issue mentioned in the problem statement"""
    
    print("Testing the shopping cart issue...")
    
    # Create a coles shopping cart as mentioned in the issue
    coles_cart = Container("coles shopping cart", 1, 1000)
    
    # Try to reproduce the wrong output: "total weight: 30, empty weight: 1, capacity: 28/1000"
    # This suggests there might be items with total weight of 29 (30 - 1 empty weight)
    # And remaining capacity of 28 out of some smaller total capacity
    
    print(f"Empty cart: {coles_cart}")
    
    # Let's add items that would give us total weight of 30
    test_items = [
        Item("item1", 10),
        Item("item2", 19)  # Total: 29, plus 1 empty weight = 30 total
    ]
    
    for item in test_items:
        coles_cart.add_item(item)
        print(f"Added {item}")
    
    print(f"Cart after adding items: {coles_cart}")
    
    # Now let's see if we can create the scenario that gives "capacity: 28/1000"
    # This doesn't make sense with our current implementation, so let's check
    # if there's a bug in the capacity calculation
    
    # Let's also try with a different cart capacity to see if we can reproduce the issue
    print("\n--- Testing with different cart capacity ---")
    small_cart = Container("coles shopping cart", 1, 57)  # If capacity was 57, then 57-29=28 remaining
    
    print(f"Small cart empty: {small_cart}")
    
    for item in test_items:
        small_cart.add_item(item)
        print(f"Added {item}")
    
    print(f"Small cart after adding items: {small_cart}")
    
    # Let's also test the scenario that would give us exactly the wrong output
    print("\n--- Testing exact wrong scenario ---")
    wrong_cart = Container("coles shopping cart", 1, 1000)
    
    # Maybe the issue is in the string representation or calculation
    # Let's manually set items to see if we can reproduce
    wrong_items = [Item("test_item", 29)]  # This should give total weight 30
    
    for item in wrong_items:
        wrong_cart.add_item(item)
    
    print(f"Wrong scenario cart: {wrong_cart}")

if __name__ == "__main__":
    test_shopping_cart_issue()