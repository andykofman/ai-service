# Testing Guide

This guide provides detailed examples for testing different aspects of the AI Service application.

## Testing the Chat System

The chat system can be tested in several ways:

### 1. Using the Web Interface
1. Visit the application at `http://localhost:8000` (or the live demo)
2. Enter your user ID (e.g., "u1")
3. Start chatting! Here are some example interactions:

```
User: Hello
Bot: Hi there! What can I do for you?

User: Show me the products
Bot: Here are our available products:
- Widget ($10)
- Gadget ($20)
Please type the name of the product you'd like to order.

User: Widget
Bot: Great! I've placed an order for Widget. Your order ID is o1. Would you like to check your order status?

User: Check my orders
Bot: Here are your orders:
Order o1: Widget - Status: pending
```

### 2. Using cURL
You can test the chat endpoint directly using cURL:

```bash
# Send a greeting
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "message": "hello"}'

# Ask about products
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "message": "what products do you have?"}'

# Check order status
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "message": "check my orders"}'
```

### 3. Using Python Requests
```python
import requests

def chat(user_id: str, message: str) -> str:
    response = requests.post(
        "http://localhost:8000/webhook",
        json={"user_id": user_id, "message": message}
    )
    return response.json()["response"]

# Example usage
print(chat("u1", "hello"))  # Get a greeting
print(chat("u1", "show products"))  # List products
print(chat("u1", "check my orders"))  # Check orders
```

### Supported Chat Intents
The chat system supports various intents including:
- Greetings and farewells
- Product browsing and ordering
- Order status checking
- General assistance

## Running Automated Tests

To run the automated test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_chat.py

# Run with verbose output
pytest -v
```

## Test Coverage

To check test coverage:

```bash
pytest --cov=app tests/
```

This will generate a coverage report showing which parts of the codebase are covered by tests.

## Writing New Tests

When writing new tests:
1. Place test files in the `tests/` directory
2. Name test files with `test_` prefix
3. Name test functions with `test_` prefix
4. Use pytest fixtures for common setup
5. Follow the Arrange-Act-Assert pattern

Example test structure:
```python
def test_chat_greeting():
    # Arrange
    user_id = "u1"
    message = "hello"
    
    # Act
    response = chat(user_id, message)
    
    # Assert
    assert "hello" in response.lower()
    assert "help" in response.lower()
``` 