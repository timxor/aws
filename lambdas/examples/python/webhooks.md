# Webhook Examples

## 1. HTTP POST Request
Webhooks are typically sent as an HTTP POST request. This is the standard method for webhook deliveries.

- **Method**: POST
- **URL**: `https://yourapp.com/webhook`
- **Headers**:
  - `Content-Type`: Usually `application/json` (if the payload is JSON) or `application/x-www-form-urlencoded` (less common).
  - `User-Agent`: Identifies the sender (e.g., "Stripe/v1").
  - `X-Signature`: A signature header for security (e.g., Stripe uses `Stripe-Signature` for HMAC verification).
- **Body** (Example Stripe payment webhook):
  ```json
  {
    "id": "evt_123456789",
    "type": "payment_intent.succeeded",
    "data": {
      "object": {
        "id": "pi_123456789",
        "amount": 1000,
        "currency": "usd",
        "status": "succeeded"
      }
    },
    "created": 1712978400
  }
