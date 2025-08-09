import csv

# ========== Exceptions ==========

# Raised when trying to store an item that exceeds container capacity
class LootCapacityError(Exception):
    pass

# ========== Base Classes ==========

# Represents a generic item that can be stored in containers
class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __str__(self):
        return f"{self.name} (weight: {self.weight})"

# Represents a container that can hold items
class Container:
    def __init__(self, name, empty_weight, capacity):
        self.name = name
        self.empty_weight = empty_weight
        self.capacity = capacity
        self.items = []
    
    def add_item(self, item):
        current_weight = sum(item.weight for item in self.items)
        if current_weight + item.weight > self.capacity:
            raise LootCapacityError(f"Adding {item.name} would exceed capacity")
        self.items.append(item)
    
    def remove_item(self, item_name):
        for i, item in enumerate(self.items):
            if item.name == item_name:
                return self.items.pop(i)
        return None
    
    def get_total_weight(self):
        items_weight = sum(item.weight for item in self.items)
        return self.empty_weight + items_weight
    
    def get_remaining_capacity(self):
        current_item_weight = sum(item.weight for item in self.items)
        return self.capacity - current_item_weight
    
    def __str__(self):
        total_weight = self.get_total_weight()
        remaining_capacity = self.get_remaining_capacity()
        # Show 0/0 when container is at full capacity
        if remaining_capacity == 0:
            capacity_str = "0/0"
        else:
            capacity_str = f"{remaining_capacity}/{self.capacity}"
        return f"A {self.name} (total weight: {total_weight}, empty weight: {self.empty_weight}, capacity: {capacity_str})"

# Magic container that can expand capacity
class MagicContainer(Container):
    def __init__(self, name, empty_weight, base_capacity, expansion_factor=2):
        super().__init__(name, empty_weight, base_capacity)
        self.base_capacity = base_capacity
        self.expansion_factor = expansion_factor
    
    def add_item(self, item):
        current_weight = sum(item.weight for item in self.items)
        if current_weight + item.weight > self.capacity:
            # Expand capacity if needed
            while current_weight + item.weight > self.capacity:
                self.capacity *= self.expansion_factor
        self.items.append(item)

# Multi-compartment container
class MultiCompartmentContainer(Container):
    def __init__(self, name, empty_weight, compartments):
        # Total capacity is sum of all compartments
        total_capacity = sum(comp['capacity'] for comp in compartments)
        super().__init__(name, empty_weight, total_capacity)
        self.compartments = {comp['name']: {'capacity': comp['capacity'], 'items': []} 
                           for comp in compartments}
    
    def add_item_to_compartment(self, item, compartment_name):
        if compartment_name not in self.compartments:
            raise ValueError(f"Compartment {compartment_name} does not exist")
        
        comp = self.compartments[compartment_name]
        current_weight = sum(item.weight for item in comp['items'])
        if current_weight + item.weight > comp['capacity']:
            raise LootCapacityError(f"Adding {item.name} would exceed {compartment_name} capacity")
        
        comp['items'].append(item)
        self.items.append(item)  # Also add to main items list

# ========== CSV Reading Functions ==========

def read_items(filename):
    items = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item = Item(row['name'], float(row['weight']))
                items.append(item)
    except FileNotFoundError:
        print(f"File {filename} not found")
    return items

def read_containers(filename):
    containers = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                container = Container(row['name'], float(row['empty_weight']), float(row['capacity']))
                containers.append(container)
    except FileNotFoundError:
        print(f"File {filename} not found")
    return containers

def read_magic_containers(filename):
    containers = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                container = MagicContainer(row['name'], float(row['empty_weight']), 
                                         float(row['base_capacity']), float(row.get('expansion_factor', 2)))
                containers.append(container)
    except FileNotFoundError:
        print(f"File {filename} not found")
    return containers

def read_multi_containers(filename):
    containers = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Parse compartments from CSV (assuming JSON-like format)
                import json
                compartments = json.loads(row['compartments'])
                container = MultiCompartmentContainer(row['name'], float(row['empty_weight']), compartments)
                containers.append(container)
    except FileNotFoundError:
        print(f"File {filename} not found")
    return containers

# ========== Helper Functions ==========

def find_by_name(items_or_containers, name):
    for item in items_or_containers:
        if item.name.lower() == name.lower():
            return item
    return None

# ========== Main Interactive CLI ==========

def main():
    # Load data from CSV files
    items = read_items('items.csv')
    containers = read_containers('containers.csv')
    magic_containers = read_magic_containers('magic_containers.csv')
    multi_containers = read_multi_containers('multi_containers.csv')
    
    all_containers = containers + magic_containers + multi_containers
    
    print("Welcome to the Inventory Management System!")
    
    # Demo: Create a coles shopping cart and demonstrate the fixed issue
    print("\n=== Shopping Cart Demo ===")
    
    # Load the coles shopping cart from CSV (with correct specifications)
    coles_cart = find_by_name(containers, "coles shopping cart")
    if not coles_cart:
        # Fallback: create with correct specifications
        coles_cart = Container("coles shopping cart", 43, 28)
    else:
        # Create a fresh instance to avoid modifying the loaded one
        coles_cart = Container(coles_cart.name, coles_cart.empty_weight, coles_cart.capacity)
    
    # Add some items to demonstrate the correct output
    demo_items = [
        Item("bread", 15),
        Item("milk", 13)  # Total: 28, exactly filling the capacity
    ]
    
    print(f"Initial cart: {coles_cart}")
    
    # Add items to cart
    for item in demo_items:
        try:
            coles_cart.add_item(item)
            print(f"Added {item}")
        except LootCapacityError as e:
            print(f"Could not add {item}: {e}")
    
    print(f"\nFinal cart: {coles_cart}")
    
    # Interactive loop
    while True:
        print("\n=== Main Menu ===")
        print("1. View all items")
        print("2. View all containers") 
        print("3. Create new container")
        print("4. Add item to container")
        print("5. Remove item from container")
        print("6. View container contents")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\n=== Available Items ===")
            for item in items:
                print(f"- {item}")
        
        elif choice == '2':
            print("\n=== Available Containers ===")
            for container in all_containers:
                print(f"- {container}")
        
        elif choice == '3':
            print("\n=== Create New Container ===")
            name = input("Enter container name: ").strip()
            try:
                empty_weight = float(input("Enter empty weight: "))
                capacity = float(input("Enter capacity: "))
                new_container = Container(name, empty_weight, capacity)
                all_containers.append(new_container)
                print(f"Created: {new_container}")
            except ValueError:
                print("Invalid input. Please enter numeric values for weight and capacity.")
        
        elif choice == '4':
            print("\n=== Add Item to Container ===")
            container_name = input("Enter container name: ").strip()
            container = find_by_name(all_containers, container_name)
            if not container:
                print("Container not found.")
                continue
            
            item_name = input("Enter item name: ").strip()
            item = find_by_name(items, item_name)
            if not item:
                # Allow creating new items on the fly
                try:
                    weight = float(input(f"Item '{item_name}' not found. Enter weight to create it: "))
                    item = Item(item_name, weight)
                    items.append(item)
                except ValueError:
                    print("Invalid weight. Skipping.")
                    continue
            
            try:
                container.add_item(item)
                print(f"Added {item} to {container.name}")
                print(f"Updated container: {container}")
            except LootCapacityError as e:
                print(f"Error: {e}")
        
        elif choice == '5':
            print("\n=== Remove Item from Container ===")
            container_name = input("Enter container name: ").strip()
            container = find_by_name(all_containers, container_name)
            if not container:
                print("Container not found.")
                continue
            
            item_name = input("Enter item name to remove: ").strip()
            removed_item = container.remove_item(item_name)
            if removed_item:
                print(f"Removed {removed_item} from {container.name}")
                print(f"Updated container: {container}")
            else:
                print("Item not found in container.")
        
        elif choice == '6':
            print("\n=== View Container Contents ===")
            container_name = input("Enter container name: ").strip()
            container = find_by_name(all_containers, container_name)
            if not container:
                print("Container not found.")
                continue
            
            print(f"\n{container}")
            if container.items:
                print("Contents:")
                for item in container.items:
                    print(f"  - {item}")
            else:
                print("Container is empty.")
        
        elif choice == '7':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()