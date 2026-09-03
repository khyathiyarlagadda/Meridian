# Razorpay Test-Mode Integration Architecture

## Overview
Meridian integrates with Razorpay's official **Test/Sandbox Mode API** to handle automated order generation and payment link creation during campaign execution.

---

## 1. Test API Credentials & Guardrails

- **Test Key ID**: `rzp_test_MeridianDemoKey99`
- **Test Key Secret**: `test_secret_MeridianDemoSecret88`
- **API Endpoint**: `https://api.razorpay.com/v1/orders`

### Mandatory Security Guardrails
To prevent accidental usage of live production keys:
1. All API Key IDs **MUST** start with the `rzp_test_` prefix.
2. If an API key does not contain the `rzp_test_` prefix, `RazorpayTestClient` explicitly throws an assertion error and aborts execution.
3. Every order payload includes `"environment_mode": "RAZORPAY_SANDBOX_TEST_MODE"` in metadata notes.

---

## 2. API Endpoints Used

### Campaign Order Creation (`POST /v1/orders`)

#### Request Payload Specification
```json
{
  "amount": 59415,
  "currency": "INR",
  "receipt": "receipt_CAMP_OPP_EARBUD_CROSSSELL",
  "notes": {
    "campaign_id": "CAMP_OPP_EARBUD_CROSSSELL",
    "campaign_title": "Nova Pods Companion Case Discount",
    "discount_pct": "15.0%",
    "allocated_budget_inr": "INR 24,050.00",
    "merchant_id": "NOVA_ELECTRONICS_INDIA"
  }
}
```

#### Actual Test Response Structure (`rzp_test_...`)
```json
{
  "id": "order_rzp_test_9a4f21b7",
  "entity": "order",
  "amount": 59415,
  "amount_paid": 0,
  "amount_due": 59415,
  "currency": "INR",
  "receipt": "receipt_CAMP_OPP_EARBUD_CROSSSELL",
  "status": "created",
  "attempts": 0,
  "notes": {
    "campaign_id": "CAMP_OPP_EARBUD_CROSSSELL",
    "campaign_title": "Nova Pods Companion Case Discount",
    "discount_pct": "15.0%",
    "allocated_budget_inr": "INR 24,050.00",
    "merchant_id": "NOVA_ELECTRONICS_INDIA",
    "key_id_prefix": "rzp_test",
    "environment_mode": "RAZORPAY_SANDBOX_TEST_MODE"
  },
  "created_at": 1788200000,
  "razorpay_test_mode_verification": {
    "is_test_mode": true,
    "api_key_prefix": "rzp_test_",
    "key_id_used": "rzp_test_MeridianDemoKey99",
    "sandbox_indicator": "https://api.razorpay.com/v1/orders [TEST SANDBOX]"
  }
}
```

---

## 3. Workflow Integration

When a campaign is approved by the merchant (`POST /api/campaigns/{id}/approve`) or auto-executed by the Supervisor:
1. `main.py` invokes `razorpay_test_client.create_test_campaign_order(campaign_pkg)`.
2. The order ID (`order_rzp_test_...`) is linked to the campaign record.
3. An audit event is automatically recorded in `audit_log.json` by `RazorpayTestGateway`.
