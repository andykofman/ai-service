# API Reference

## Users
- `GET /users` – list all users
- `POST /users` – create a user
  ```json
  {
    "user_id": "u1",
    "name": "Jane",
    "email": "jane@example.com"
  }
  ```

## Products
- `GET /products` – list all products
- `POST /products` – create a product
  ```json
  {
    "product_id": "p1",
    "name": "Widget",
    "price": 10,
    "description": "Small widget"
  }
  ```

## Orders
- `GET /orders` – list all orders
- `GET /orders/{order_id}` – get one order
- `POST /orders` – create an order
  ```json
  {
    "order_id": "o1",
    "user_id": "u1",
    "product_id": "p1",
    "quantity": 1,
    "status": "pending"
  }
  ```

## Chat Webhook
- `POST /webhook` – send a message to the assistant
  ```json
  {
    "user_id": "u1",
    "message": "hello"
  }
  ```
  Returns `{ "response": "..." }`.
