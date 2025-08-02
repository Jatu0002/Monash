#!/usr/bin/env python3

from inventory import Container, Item

def test_full_capacity():
    """Test what happens when a container is at full capacity"""
    
    print("=== Testing Full Capacity Behavior ===")
    
    # Create a cart that matches issue #3 specifications
    cart = Container("coles shopping cart", 43, 28)
    
    print(f"Empty cart: {cart}")
    
    # Add items up to exactly the capacity
    items = [
        Item("item1", 14),
        Item("item2", 14)  # Total: 28, exactly the capacity
    ]
    
    for item in items:
        cart.add_item(item)
        print(f"Added {item}")
        print(f"Current cart: {cart}")
    
    print(f"\nFinal cart (should be at capacity): {cart}")
    
    # Verify the numbers
    print(f"\nVerification:")
    print(f"Empty weight: {cart.empty_weight}")
    print(f"Items weight: {sum(item.weight for item in cart.items)}")
    print(f"Total weight: {cart.get_total_weight()}")
    print(f"Capacity: {cart.capacity}")
    print(f"Remaining capacity: {cart.get_remaining_capacity()}")
    
    # The issue might be that the expected format "0/0" means something different
    # Maybe it means "remaining/available" instead of "remaining/total"?
    
    print(f"\nDifferent interpretation test:")
    # What if "capacity: 0/0" means when both remaining and available are 0?
    # That doesn't make sense either...
    
    # Let me check if the issue is that when full, it should show differently
    if cart.get_remaining_capacity() == 0:
        print("Cart is at full capacity!")
        # Maybe the expected format is to show 0/0 when full?

if __name__ == "__main__":
    test_full_capacity()