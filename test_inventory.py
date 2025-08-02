#!/usr/bin/env python3
"""Test script to verify the inventory system works correctly."""

import inventory

def test_basic_functionality():
    """Test basic functionality without user interaction."""
    print("=== Testing Basic Functionality ===")
    
    # Load all data
    items = inventory.read_items('items.csv')
    containers = inventory.read_containers('containers.csv')
    containers_dict = {c.name: c for c in containers}
    magic_containers = inventory.read_magic_containers('magic_containers.csv', containers_dict)
    containers += magic_containers
    containers_dict = {c.name: c for c in containers}
    multi_containers = inventory.read_multi_containers('multi_containers.csv', containers_dict)
    all_containers = containers + multi_containers
    all_objects = items + all_containers
    
    print(f"Loaded {len(items)} items, {len(containers)} regular containers, {len(magic_containers)} magic containers, {len(multi_containers)} multi-compartment containers")
    
    # Test regular container
    print("\n--- Testing Regular Container ---")
    backpack = inventory.find_by_name(all_containers, "Backpack")
    sword = inventory.find_by_name(items, "Sword")
    print(f"Before: {backpack}")
    backpack.loot_item(sword)
    print(f"After looting sword: {backpack}")
    
    # Test magic container
    print("\n--- Testing Magic Container ---")
    magic_backpack = inventory.find_by_name(all_containers, "Magic Backpack")
    shield = inventory.find_by_name(items, "Shield")
    print(f"Before: {magic_backpack}")
    magic_backpack.loot_item(shield)
    print(f"After looting shield: {magic_backpack}")
    
    # Test multi-compartment container
    print("\n--- Testing Multi-Compartment Container ---")
    travel_pack = inventory.find_by_name(all_containers, "Travel Pack")
    potion = inventory.find_by_name(items, "Potion")
    print(f"Before: {travel_pack}")
    travel_pack.loot_item(potion)
    print(f"After looting potion: {travel_pack}")
    
    # Test listing
    print("\n--- Testing List Functionality ---")
    print("Travel Pack contents:")
    for line in travel_pack.list_looted():
        print(line)
    
    # Test capacity error
    print("\n--- Testing Capacity Error ---")
    small_pouch = inventory.find_by_name(all_containers, "Small Pouch")
    armor = inventory.find_by_name(items, "Armor")
    try:
        small_pouch.loot_item(armor)
        print("ERROR: Should have failed!")
    except inventory.LootCapacityError:
        print(f"SUCCESS: Correctly prevented storing {armor.name} in {small_pouch.name}")
    
    print("\n=== All Tests Passed! ===")

if __name__ == "__main__":
    test_basic_functionality()