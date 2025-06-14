# Test Pictures Organization

This directory contains screenshots and visual documentation of the system's testing process, organized by purpose and chronological order.

## Directory Structure

```
tests/pics/
├── 01-system-overview/           # Basic system structure and user interface
│   ├── Structure.png            # Overall system architecture
│   └── All_user.png             # User interface overview
│
├── 02-database-monitoring/       # Database interaction and monitoring
│   ├── DBeaver.png              # Database management interface
│   ├── User.png                 # User data view
│   ├── Real_user.png            # Real user interaction view
│   └── Conversation.png         # Conversation data view
│
└── 03-test-data/                # Test data and responses
    ├── Dummy_intent.png         # Test intent data
    └── Dummy_response.png       # Test response data
```

## Organization Rationale

1. **01-system-overview/**
   - Contains high-level system architecture and interface screenshots
   - Shows the basic structure and user interface components
   - These are typically the first screenshots taken during testing

2. **02-database-monitoring/**
   - Contains screenshots related to database interactions
   - Shows how the system handles data storage and retrieval
   - Includes both management interface and user interaction views

3. **03-test-data/**
   - Contains screenshots of test data and responses
   - Shows how the system handles test scenarios
   - Demonstrates the system's response to various inputs

## Naming Convention

- Directories are prefixed with numbers to indicate their chronological order
- File names are descriptive of their content
- All files use lowercase with underscores for spaces
- PNG format is used for all screenshots to maintain quality

## Usage

These pictures serve as visual documentation for:
- System/Unit testing
- User interface verification
- Database interaction validation
- Test case documentation

## Example: Order and Product Relationship

The following images in `02-database-monitoring/` demonstrate how an order references a product in the database:

- **Order Entry:**  
  `order_with_product_reference.png`
- **Product Details:**  
  `product_details_for_order.png`

As shown, the `product_id` in the order matches the `product_id` in the products table, linking the order to the specific product.

### Entity Relationship Diagram

```mermaid
erDiagram
    ORDERS {
        string order_id
        string user_id
        string product_id
        int quantity
        string status
    }
    PRODUCTS {
        string product_id
        string name
        int price
        string description
    }
    ORDERS ||--o{ PRODUCTS : "references"
```

This visual and diagrammatic documentation helps clarify the connection between orders and products in your system's database.

