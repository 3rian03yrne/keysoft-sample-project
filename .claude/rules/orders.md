---
paths: ["src/orders/**"]
---
# Order-domain rules — scoped so they never clutter unrelated prompts.
- Keep the api.py handlers thin: validate input, then delegate to service.py.
- Log the action taken (logger.info) so cancellations and refunds stay auditable.