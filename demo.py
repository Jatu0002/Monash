#!/usr/bin/env python3
"""
Comprehensive demonstration of the inventory management system.
This script showcases all features of the system without requiring user interaction.
"""

import inventory

def demonstrate_system():
    """Demonstrate all features of the inventory management system."""
    print("=" * 60)
    print("INVENTORY MANAGEMENT SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Load all data
    print("\n1. LOADING DATA FROM CSV FILES")
    print("-" * 40)
    items = inventory.read_items('items.csv')
    containers = inventory.read_containers('containers.csv')
    containers_dict = {c.name: c for c in containers}
    magic_containers = inventory.read_magic_containers('magic_containers.csv', containers_dict)
    containers += magic_containers
    containers_dict = {c.name: c for c in containers}
    multi_containers = inventory.read_multi_containers('multi_containers.csv', containers_dict)
    all_containers = containers + multi_containers
    all_objects = items + all_containers
    
    print(f"✓ Loaded {len(items)} items")
    print(f"✓ Loaded {len(containers)} containers (including {len(magic_containers)} magic containers)")
    print(f"✓ Loaded {len(multi_containers)} multi-compartment containers")
    print(f"✓ Total objects: {len(all_objects)}")
    
    # Show available items
    print("\n2. AVAILABLE ITEMS")
    print("-" * 40)
    for item in items:
        print(f"  • {item}")
    
    # Show available containers
    print("\n3. AVAILABLE CONTAINERS")
    print("-" * 40)
    for container in all_containers:
        print(f"  • {container}")
    
    # Demonstrate regular container
    print("\n4. REGULAR CONTAINER DEMONSTRATION")
    print("-" * 40)
    backpack = inventory.find_by_name(all_containers, "Backpack")
    sword = inventory.find_by_name(items, "Sword")
    shield = inventory.find_by_name(items, "Shield")
    helmet = inventory.find_by_name(items, "Helmet")
    
    print(f"Selected container: {backpack}")
    print(f"Items to loot: {sword}, {shield}, {helmet}")
    
    print(f"\n  Before looting: {backpack}")
    backpack.loot_item(sword)
    print(f"  After sword:    {backpack}")
    backpack.loot_item(shield)
    print(f"  After shield:   {backpack}")
    backpack.loot_item(helmet)
    print(f"  After helmet:   {backpack}")
    
    print("\n  Final contents:")
    for line in backpack.list_looted():
        print(f"    {line}")
    
    # Demonstrate magic container
    print("\n5. MAGIC CONTAINER DEMONSTRATION")
    print("-" * 40)
    magic_backpack = inventory.find_by_name(all_containers, "Magic Backpack")
    bow = inventory.find_by_name(items, "Bow")
    armor = inventory.find_by_name(items, "Armor")
    book = inventory.find_by_name(items, "Book")
    
    print(f"Selected magic container: {magic_backpack}")
    print(f"Items to loot: {bow}, {armor}, {book}")
    print("Note: Magic containers don't add item weight to total weight!")
    
    print(f"\n  Before looting: {magic_backpack}")
    magic_backpack.loot_item(bow)
    print(f"  After bow:      {magic_backpack}")
    magic_backpack.loot_item(armor)
    print(f"  After armor:    {magic_backpack}")
    magic_backpack.loot_item(book)
    print(f"  After book:     {magic_backpack}")
    
    print("\n  Final contents:")
    for line in magic_backpack.list_looted():
        print(f"    {line}")
    
    # Demonstrate multi-compartment container
    print("\n6. MULTI-COMPARTMENT CONTAINER DEMONSTRATION")
    print("-" * 40)
    travel_pack = inventory.find_by_name(all_containers, "Travel Pack")
    potion = inventory.find_by_name(items, "Potion")
    gem = inventory.find_by_name(items, "Gem")
    gold_coin = inventory.find_by_name(items, "Gold Coin")
    arrow = inventory.find_by_name(items, "Arrow")
    
    print(f"Selected multi-compartment container: {travel_pack}")
    print(f"Items to loot: {potion}, {gem}, {gold_coin}, {arrow}")
    print("Note: Items are stored in the first compartment that can fit them!")
    
    print(f"\n  Before looting: {travel_pack}")
    travel_pack.loot_item(potion)
    print(f"  After potion:   {travel_pack}")
    travel_pack.loot_item(gem)
    print(f"  After gem:      {travel_pack}")
    travel_pack.loot_item(gold_coin)
    print(f"  After coin:     {travel_pack}")
    travel_pack.loot_item(arrow)
    print(f"  After arrow:    {travel_pack}")
    
    print("\n  Final contents:")
    for line in travel_pack.list_looted():
        print(f"    {line}")
    
    # Demonstrate capacity error
    print("\n7. CAPACITY ERROR DEMONSTRATION")
    print("-" * 40)
    small_pouch = inventory.find_by_name(all_containers, "Small Pouch")
    large_armor = inventory.find_by_name(items, "Armor")
    
    print(f"Trying to store {large_armor} in {small_pouch}")
    print(f"Can store? {small_pouch.can_store(large_armor)}")
    
    try:
        small_pouch.loot_item(large_armor)
        print("❌ ERROR: Should have failed!")
    except inventory.LootCapacityError:
        print("✓ SUCCESS: Correctly prevented storage due to capacity limit")
    
    # Show final system state
    print("\n8. FINAL SYSTEM STATE")
    print("-" * 40)
    print("All containers with their contents:")
    for container in all_containers:
        if hasattr(container, 'contents') and container.contents:
            print(f"\n{container.name}:")
            for line in container.list_looted():
                print(f"  {line}")
        elif hasattr(container, 'compartments'):
            has_items = any(hasattr(comp, 'contents') and comp.contents for comp in container.compartments)
            if has_items:
                print(f"\n{container.name}:")
                for line in container.list_looted():
                    print(f"  {line}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE!")
    print("The inventory management system is working perfectly!")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_system()