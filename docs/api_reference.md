# API Reference

## Users
- `GET /users` – List all users
- `POST /users` – Create a new user

## Products
- `GET /products` – List all products
- `POST /products` – Create a new product

## Orders
- `GET /orders` – List all orders
- `GET /orders/{order_id}` – Retrieve a single order
- `POST /orders` – Create an order

## Chat Webhook
- `POST /webhook` – Main interaction endpoint used by the sample chat client. Payload:
  ```json
  {
    "user_id": "string",
    "message": "string"
  }
  ```
  Returns `{ "response": "..." }` with the assistant reply.
