class ColesShoppingCart:
    """A shopping cart implementation for Coles supermarket."""
    
    def __init__(self, empty_weight=43, max_capacity=0):
        """Initialize a shopping cart.
        
        Args:
            empty_weight (int): The weight of the empty cart in kg
            max_capacity (int): The maximum capacity of the cart
        """
        self.empty_weight = empty_weight
        self.max_capacity = max_capacity
        self.current_capacity = 0
        self.items = []
        self.items_weight = 0
    
    def add_item(self, item_name, weight):
        """Add an item to the cart.
        
        Args:
            item_name (str): Name of the item
            weight (int): Weight of the item in kg
        """
        self.items.append((item_name, weight))
        self.items_weight += weight
    
    @property
    def total_weight(self):
        """Calculate the total weight of the cart including items."""
        return self.empty_weight + self.items_weight
    
    def __str__(self):
        """Return string representation of the shopping cart."""
        capacity_str = f"{self.current_capacity}/{self.max_capacity}"
        return f"A coles shopping cart (total weight: {self.total_weight}, empty weight: {self.empty_weight}, capacity: {capacity_str})"


def main():
    """Demo function to show the cart output."""
    # Create a cart that matches the expected output
    cart = ColesShoppingCart(empty_weight=43, max_capacity=0)
    
    # Add items to get total weight of 71
    cart.add_item("groceries", 28)  # 43 + 28 = 71
    
    print(cart)


if __name__ == "__main__":
    main()