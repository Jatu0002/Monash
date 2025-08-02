# Monash Shopping Cart

This repository contains a shopping cart implementation for Coles supermarket.

## Files

- `shopping_cart.py` - Main implementation of the ColesShoppingCart class
- `test_shopping_cart.py` - Unit tests for the shopping cart implementation

## Usage

Run the main script to see the shopping cart output:
```bash
python shopping_cart.py
```

Expected output:
```
A coles shopping cart (total weight: 71, empty weight: 43, capacity: 0/0)
```

Run the tests:
```bash
python test_shopping_cart.py
```

## Implementation Details

The `ColesShoppingCart` class provides:
- Empty weight and capacity tracking
- Item addition functionality
- Automatic total weight calculation
- Formatted string representation matching the required output format