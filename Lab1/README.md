# Lab 1: Requirements Engineering & UML Use-Case Modelling

**Scenario:** Self-Service Coffee Kiosk (the scenario that the handout's given FR-001, FR-002 and NFR-001 come from).

## Files

| File | Deliverable |
|------|-------------|
| `Lab1_Requirements_Table.xlsx` / `.docx` / `.pdf` | 1. Requirements table: 5 FRs + 2 NFRs, each with ID, Type, Description, Priority, Acceptance Criteria, Rationale and Comments |
| `UseCaseDiagram_CoffeeKiosk.pdf` (`.png`) | 2. UML use-case diagram |
| `UseCaseDiagram_CoffeeKiosk.drawio` | Editable source (open in draw.io / app.diagrams.net) |
| `Lab1_UseCase_Flow.docx` / `.pdf` | 3. One-page use-case flow for UC-03 Place Order |

## Step 4: Actors and use cases

**Actors (3):** Customer (primary), Payment Gateway («system»), Receipt Printer («device»)

| ID | Use case | From requirement |
|----|----------|------------------|
| UC-01 | Select Coffee Type | FR-001 |
| UC-02 | Select Drink Size | FR-002 |
| UC-03 | Place Order (review summary & total) | FR-003, NFR-001 |
| UC-04 | Pay by Credit Card | FR-004, NFR-002 |
| UC-05 | Print Receipt | FR-005 |
| UC-06 | Handle Declined Payment | FR-004 (retry rule) |

**Relationships:** UC-03 «include» UC-01, UC-02, UC-04, UC-05; UC-06 «extend» UC-04 (condition: card is declined).
