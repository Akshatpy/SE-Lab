# Software Engineering Lab 01: Requirements Engineering & UML Use-Case Modelling

**Course**: Software Engineering Lab (CSE 5A)  
**Student Name**: Akshat  
**Problem Statement #42**: Developer Tools & IT Operations - Internal Microservice Catalog & Health Portal  

---

## Overview

This directory contains the completed assignment deliverables for **Lab 1: Requirements Engineering & UML Use-Case Modelling**. 

The goal of this project is to analyze an enterprise developer portal scenario, capture explicit functional and non-functional requirements in standard SRS format, model user-system interactions using UML Use-Case diagrams, and document a detailed use-case flow for periodic microservice health monitoring.

---

## Submission PDF Deliverables

All required submission documents have been generated and included as ready-to-submit PDFs inside this folder:

1. 📄 **[`Requirements_Table.pdf`](Requirements_Table.pdf)**  
   Contains 5 Functional Requirements (FR-001 to FR-005) and 2 Non-Functional Requirements (NFR-001 & NFR-002) formatted with ID, Type, Description, Priority, Acceptance Criteria, Rationale, and Comments.
2. 📄 **[`Use_Case_Diagram.pdf`](Use_Case_Diagram.pdf)**  
   A UML Use-Case Diagram mapping all key actors (`DevOps Engineer`, `System Architect`, `Developer`, `Automated Health Checker`), primary use cases (`UC-01` to `UC-06`), and `«include»` / `«extend»` relationships.
3. 📄 **[`Use_Case_Flow_Specification.pdf`](Use_Case_Flow_Specification.pdf)**  
   A 1-page specification document for **UC-02: Monitor Microservice Health**, covering preconditions, postconditions, step-by-step main success scenario, and alternate downtime/failure flows.

---

## System Context & Stakeholders

### Target Stakeholders / Actors
- **DevOps Engineer**: Registers new microservices, sets up health check endpoints, views live portal status, and receives downtime alerts.
- **System Architect**: Uses the interactive dependency graph to analyze service topologies, detect bottlenecks, and evaluate failure blast radiuses.
- **Developer**: Searches the microservice catalog and inspects aggregated OpenAPI/Swagger documentation.
- **Automated Health Checker**: Background system actor executing scheduled 30-second health check probes against registered endpoints.

---

## 1. Requirements Specification Table

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Functional | The system shall ping microservice health endpoints at 30-second intervals and compute rolling 24-hour service availability percentages. | High | **Pass**: Downtime recorded and alert dispatched on 3 consecutive failed health probes.<br>**Fail**: Unreachable service marked healthy. | Core health monitoring functionality to ensure timely detection of service outages. | Baseline requirement from problem statement. |
| **FR-002** | Functional | The system shall allow a DevOps Engineer to register a new microservice by specifying its name, owner team, repository URL, API doc endpoint, and health check URL. | High | **Pass**: Service entry is added to catalog, API endpoint is validated, and initial health check is initiated within 5s.<br>**Fail**: Service registered with invalid or unreachable health endpoint without returning an error. | Essential for building and keeping the service catalog up to date. | Input validation required for endpoint URLs. |
| **FR-003** | Functional | The system shall visualize microservice dependencies as an interactive dependency graph mapping upstream and downstream service connections based on registered metadata. | High | **Pass**: Graph accurately renders all service nodes and dependency edges, allowing filtering by environment or status.<br>**Fail**: Circular or missing dependencies cause visual graph rendering errors. | Enables System Architects to analyze topology and assess blast radius of service failures. | Node graph should support panning and zooming. |
| **FR-004** | Functional | The system shall dispatch real-time downtime notifications to DevOps Engineers via email and Slack webhook when a service health status changes to 'Unhealthy'. | Medium | **Pass**: Notification delivered to designated Slack channel and email list within 10 seconds of health check failure.<br>**Fail**: Alert lost or delayed beyond 30 seconds. | Reduces Mean Time to Detection (MTTD) for operational incidents. | Include alert rate limiting to avoid notification spam. |
| **FR-005** | Functional | The system shall aggregate and display searchable API documentation (OpenAPI/Swagger specs) for all registered microservices. | Medium | **Pass**: Developers can search by service name or keyword and view rendered API endpoint details.<br>**Fail**: API documentation page fails to render or shows stale schema. | Enables Developers to easily discover and consume internal APIs without contacting team leads. | Support OpenAPI 3.0 specs. |
| **NFR-001** | Non-Functional (Performance) | The service catalog dependency graph viewer must render interactive node architectures containing up to 200 services smoothly without UI degradation. | High | **Pass**: Benchmarking tests confirm target latency (< 2.0s render time) and smooth 60 FPS interactions under simulated peak load (200 nodes, 500 edges).<br>**Fail**: Page freezes or rendering time exceeds 3.0 seconds. | Ensures System Architects can navigate large enterprise microservice topologies effectively. | Baseline requirement from problem statement. |
| **NFR-002** | Non-Functional (Security & Availability) | The system shall enforce Role-Based Access Control (RBAC) via enterprise OAuth2/SSO and maintain 99.9% portal uptime during operational hours. | High | **Pass**: Unauthorized write attempts are blocked with HTTP 403, and 30-day portal uptime meets or exceeds 99.9%.<br>**Fail**: Unauthorized user creates/edits catalog entries or portal availability drops below 99.9%. | Protects internal service configuration integrity and guarantees system availability for DevOps teams. | Integrate with enterprise SSO (Okta / Azure AD). |

---

## 2. UML Use-Case Modeling

- **Primary Use Cases**:
  - `UC-01`: Register Microservice
  - `UC-02`: Monitor Microservice Health
  - `UC-03`: View Dependency Graph
  - `UC-04`: View API Documentation
  - `UC-05`: Send Downtime Alerts
  - `UC-06`: Execute Health Probe
- **Relationships**:
  - `UC-02` **`«include»`** `UC-06` (Monitoring health always executes a health check probe).
  - `UC-05` **`«extend»`** `UC-02` (Downtime alerts are dispatched conditionally when 3 consecutive probes fail).

---

## 3. Use-Case Flow Summary (UC-02)

- **Preconditions**: Microservice registered with valid health check endpoint; background checker active.
- **Main Success Steps**:
  1. Trigger 30-second health check schedule.
  2. Retrieve list of active services and health check URLs.
  3. Send HTTP GET health probe.
  4. Microservice responds with `HTTP 200 OK` within 3 seconds.
  5. Mark service status as `Healthy` and log response latency.
  6. Recalculate 24-hour service availability percentage.
  7. Refresh live dashboard for DevOps Engineers.
- **Alternate Flow (Downtime Handling)**:
  - If a probe fails, increment failure counter.
  - On 3 consecutive failures, set status to `Unhealthy`, log incident, and invoke `«extend»` **UC-05: Send Downtime Alerts** via Slack/Email.
