# Lab 3: Component Modelling & Architectural Pattern Selection

**Scenario:** Self-Service Coffee Kiosk (3 coffee types, 2 sizes, credit card only, printed receipt; touch screen, receipt printer and stored menu/prices).

## Files

| File | Deliverable |
|------|-------------|
| `ComponentDiagram_CoffeeKiosk.png` / `.pdf` | 1. Component diagram |
| `ComponentDiagram_CoffeeKiosk.drawio` | Editable source (open in draw.io / app.diagrams.net) |
| `Lab3_Architecture_Justification.docx` / `.pdf` | 2. One-page written justification |

## Step 1: Key requirements and challenges

- **Functional:** select type, select size, show total, pay by card, print receipt.
- **Non-functional:** fast ordering (< 60 s, peak hours), card data security, works with kiosk hardware.
- **Challenges:** *performance*, because every tap must respond instantly; *usability*, because it is a touch UI for walk-up customers; *security*, because card data must reach only the payment gateway.

## Step 2: Architectural style analysis

| Style | Fit for the kiosk | Pros here | Cons here |
|-------|-------------------|-----------|-----------|
| **Layered** ✅ | Single self-contained device with clear UI / logic / data / hardware concerns | Clear separation; hardware isolated behind interfaces; fast in-process calls; simple to build and test | Every request passes through the layers (negligible at this size); scaling single components isn't needed |
| Microservices | Over-engineered | Independent deployment/scaling, fault isolation | Network latency between services on one box, operational overhead, distributed data consistency for a 6-item menu |
| Client-Server | Weak | Central menu/price control across many kiosks | Kiosk stops working if server/network is down (single point of failure); every tap needs a network round-trip |

**Selected:** Layered.

## Step 3: Components

| # | Component | Layer | Source |
|---|-----------|-------|--------|
| 1 | Order Manager | Business | given |
| 2 | Payment Service | Business | given |
| 3 | Touch Screen UI | Presentation | identified (touch-screen constraint) |
| 4 | Menu & Pricing Repository | Data | identified (menu/pricing storage constraint) |
| 5 | Receipt Printer Driver | Hardware Abstraction | identified (receipt printer constraint) |
| – | Card Payment Gateway | external system | provides card authorization |

## Step 4: Interfaces (ball = provider, socket = requirer)

| Interface | Provided by | Required by | Protocol / technology |
|-----------|-------------|-------------|-----------------------|
| IOrderService | Order Manager | Touch Screen UI | in-process API call |
| IPaymentService *(given)* | Payment Service | Order Manager | API call: payment processing requests |
| IMenuData | Menu & Pricing Repository | Order Manager | SQL queries (SQLite) |
| IReceiptPrinter | Receipt Printer Driver | Order Manager | hardware API: ESC/POS over USB |
| ICardAuthorization | Card Payment Gateway | Payment Service | HTTPS REST (TLS 1.2+) |
