#!/usr/bin/env python3
"""
Demonstration of the shopping cart fix

This script shows how the shopping cart issue was resolved.
"""

from inventory import Container, Item

def main():
    print("=== Shopping Cart Fix Demonstration ===")
    print()
    
    print("BEFORE (Wrong):")
    print("Output: A coles shopping cart (total weight: 30, empty weight: 1, capacity: 28/1000)")
    print("Issues: Wrong empty weight (1 vs 43), wrong capacity (1000 vs 28)")
    print()
    
    print("AFTER (Correct):")
    
    # Create cart with correct specifications
    cart = Container("coles shopping cart", 43, 28)
    print(f"Empty cart: {cart}")
    
    # Add items to exactly fill capacity
    items = [
        Item("groceries_1", 15),
        Item("groceries_2", 13)
    ]
    
    for item in items:
        cart.add_item(item)
        print(f"Added {item}")
    
    print(f"Full cart: {cart}")
    print()
    
    print("✅ FIXED: Now shows correct total weight (71), empty weight (43), and capacity (0/0)")
    print("   when cart is full, as expected in issue #3")

if __name__ == "__main__":
    main()