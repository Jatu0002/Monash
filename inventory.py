import csv

# ========== Exceptions ==========

# Raised when trying to store an item that exceeds container capacity
class LootCapacityError(Exception):
    pass

# ========== Base Classes ==========

# Represents a generic item with a name and weight
class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = int(weight)

    def __str__(self):
        return f"{self.name} (weight: {self.weight})"

# Represents a container that can hold items, inherits from Item
class Container(Item):
    def __init__(self, name, empty_weight, capacity):
        super().__init__(name, empty_weight)  # Treats empty_weight as the weight of the base item
        self.empty_weight = int(empty_weight) # Weight of the empty container
        self.capacity = int(capacity)         # Max weight that can be stored inside
        self.contents = []                   # List of items inside the container

    # Returns the sum of the empty weight and the total weight of contained items
    def total_weight(self):
        return self.empty_weight + sum(obj.weight for obj in self.contents)

    # Returns the current used capacity (sum of contained item weights)
    def current_capacity(self):
        return sum(obj.weight for obj in self.contents)

    # Checks if a new item can be added without exceeding capacity
    def can_store(self, item):
        return (self.current_capacity() + item.weight) <= self.capacity

    # Tries to add an item; raises if not enough capacity
    def loot_item(self, item):
        if not self.can_store(item):
            raise LootCapacityError()
        self.contents.append(item)

    # Pretty-print all contents recursively, with indentation
    def list_looted(self, indent=0):
        lines = [("   " * indent) + str(self)]
        for obj in self.contents:
            lines.append(("   " * (indent+1)) + str(obj))
        return lines

    # String representation, including weight and capacity info
    def __str__(self):
        return (f"{self.name} (total weight: {self.total_weight()}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_capacity()}/{self.capacity})")

# ========== Magic Container ==========

# Special container whose contents do not add to its total weight
class MagicContainer(Container):
    # Override: total weight is always just the empty weight
    def total_weight(self):
        return self.empty_weight  # No added weight from contents

    def __str__(self):
        return (f"{self.name} (total weight: {self.total_weight()}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_capacity()}/{self.capacity})")

# ========== Multi-Compartment Container ==========

# Container made up of other containers ("compartments")
class MultiCompartmentContainer(Container):
    def __init__(self, name, compartments):
        self.compartments = compartments
        empty_weight = sum(c.empty_weight for c in compartments) # Sum empty weights of all compartments
        super().__init__(name, empty_weight, 0) # Capacity set to 0; handled by compartments

    # Total weight is empty weight plus the total weights of all compartments
    def total_weight(self):
        return self.empty_weight + sum(c.total_weight() for c in self.compartments)

    # Used capacity is the sum of all compartments' used capacity
    def current_capacity(self):
        return sum(c.current_capacity() for c in self.compartments)

    # Sum of all compartments' maximum capacities
    def total_capacity(self):
        return sum(c.capacity for c in self.compartments)

    # Checks if any compartment can store the item
    def can_store(self, item):
        return any(c.can_store(item) for c in self.compartments)

    # Tries to loot the item into the first compartment that can store it
    def loot_item(self, item):
        for c in self.compartments:
            if c.can_store(item):
                c.loot_item(item)
                return
        raise LootCapacityError()

    # Pretty-print all compartments and their contents, recursively
    def list_looted(self, indent=0):
        lines = [("   " * indent) + str(self)]
        for c in self.compartments:
            lines.extend(c.list_looted(indent + 1))
        return lines

    # String representation, using total_capacity for "max"
    def __str__(self):
        return (f"{self.name} (total weight: {self.total_weight()}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_capacity()}/{self.total_capacity()})")

# ========== Readers ==========

# Reads items from a CSV file and returns a list of Item objects
def read_items(filename):
    items = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [f.strip().lower() for f in reader.fieldnames if f is not None]
        for row in reader:
            row = {k.strip().lower(): v for k, v in row.items() if k is not None}
            items.append(Item(row['name'], row['weight']))
    return items

# Reads containers from a CSV file and returns a list of Container objects
def read_containers(filename):
    containers = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [f.strip().lower().replace(' ', '_') for f in reader.fieldnames if f is not None]
        for row in reader:
            row = {k.strip().lower().replace(' ', '_'): v for k, v in row.items() if k is not None}
            containers.append(Container(row['name'], row['empty_weight'], row['weight_capacity']))
    return containers

# Reads magic containers from CSV and returns a list of MagicContainer objects
def read_magic_containers(filename, all_containers_dict):
    magic = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [f.strip().lower().replace(' ', '_') for f in reader.fieldnames if f is not None]
        for row in reader:
            row = {k.strip().lower().replace(' ', '_'): v.strip() for k, v in row.items() if k is not None}
            magic_name = row['name']
            base_name = row['container']
            base = all_containers_dict.get(base_name)
            if base is None:
                raise ValueError(f'Base container "{base_name}" not found for magic container "{magic_name}".')
            magic.append(MagicContainer(magic_name, base.empty_weight, base.capacity))
    return magic

# Reads multi-compartment containers from CSV and returns a list of MultiCompartmentContainer objects
def read_multi_containers(filename, all_containers_dict):
    multi = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [f.strip().lower().replace(' ', '_') for f in reader.fieldnames if f is not None]
        for row in reader:
            row = {k.strip().lower().replace(' ', '_'): v for k, v in row.items() if k is not None}
            field_key = 'compartments' if 'compartments' in row else 'containers' if 'containers' in row else None
            if not field_key:
                raise KeyError(f"'compartments' or 'containers' field missing in row: {row}")
            compartment_names = [name.strip() for name in row[field_key].split(',')]
            compartments = []
            for cname in compartment_names:
                base = all_containers_dict.get(cname)
                if base is None:
                    raise ValueError(f'Compartment "{cname}" not found for multi-container "{row["name"]}"')
                # Each compartment is a copy of the base container
                compartments.append(Container(base.name, base.empty_weight, base.capacity))
            multi.append(MultiCompartmentContainer(row['name'], compartments))
    return multi

# =========== Helper ==========

# Finds and returns the first object in a sequence with a matching name
def find_by_name(seq, name):
    for obj in seq:
        if obj.name == name:
            return obj
    return None

# ========== Main ==========

def main():
    # Load all items and containers (including magic and multi-compartment)
    items = read_items('items.csv')
    containers = read_containers('containers.csv')
    containers_dict = {c.name: c for c in containers}
    magic_containers = read_magic_containers('magic_containers.csv', containers_dict)
    containers += magic_containers
    containers_dict = {c.name: c for c in containers}  # refresh dict
    multi_containers = read_multi_containers('multi_containers.csv', containers_dict)
    all_containers = containers + multi_containers
    all_objects = items + all_containers

    print(f"Initialised {len(all_objects)} items including {len(all_containers)} containers.\n")

    # Prompt user to select a container by name
    selected_container = None
    while selected_container is None:
        name = input("Enter the name of the container: ")
        found = find_by_name(all_containers, name)
        if found is None:
            print(f'"{name}" not found. Try again.')
        else:
            selected_container = found

    # Main user menu loop
    while True:
        print("==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")
        choice = input().strip()
        if choice == "0":
            break
        elif choice == "1":
            # Loot an item by name
            item_name = input("Enter the name of the item: ")
            item = find_by_name(items, item_name)
            if item is None:
                print(f'"{item_name}" not found. Try again.')
            else:
                try:
                    selected_container.loot_item(item)
                    print(f'Success! Item "{item.name}" stored in container "{selected_container.name}".')
                except LootCapacityError:
                    print(f'Failure! Item "{item.name}" NOT stored in container "{selected_container.name}".')
        elif choice == "2":
            # List all looted items in the selected container
            for line in selected_container.list_looted():
                print(line)

# Entry point for the program
if __name__ == '__main__':
    main()