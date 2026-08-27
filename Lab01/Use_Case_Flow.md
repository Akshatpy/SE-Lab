# Use-Case Flow Specification

**System**: Internal Microservice Catalog & Health Portal  
**Problem Statement**: #42 - Developer Tools & IT Operations  

---

## Use Case ID & Name: UC-02 - Monitor Microservice Health

### 1. Primary Actor
- **Automated Health Checker** (System Actor)
- **DevOps Engineer** (Secondary Actor / Notification Recipient)

### 2. Description
The system automatically monitors registered microservices by periodically pinging their health check endpoints at 30-second intervals, computing rolling 24-hour availability metrics, and triggering downtime alerts when failures are detected.

### 3. Preconditions
1. The microservice is registered in the catalog with a valid health endpoint URL (e.g., `https://service.internal/health`).
2. The background automated health monitoring service is active and running.

### 4. Postconditions
1. The current status (`Healthy` / `Unhealthy`) and latency of the microservice are updated in the system database.
2. The rolling 24-hour service availability percentage is updated.
3. If 3 consecutive failures occur, an incident log is created and downtime notifications are dispatched to DevOps Engineers.

---

### 5. Main Success Scenario (Step-by-Step)

1. **Trigger**: The Automated Health Checker scheduler initiates a health check cycle at the 30-second interval.
2. **Fetch Endpoints**: The system retrieves the list of active microservices and their registered health check endpoints from the catalog.
3. **Dispatch Probe**: The system sends an HTTP GET request to the microservice health endpoint.
4. **Receive Response**: The target microservice responds with an `HTTP 200 OK` status code and a valid payload within 3 seconds.
5. **Update Status**: The system records the probe as successful, marks the microservice status as `Healthy`, and records the response latency.
6. **Calculate Availability**: The system recalculates the rolling 24-hour uptime percentage using the updated probe logs.
7. **Refresh Dashboard**: The system updates the live health monitoring dashboard for DevOps Engineers.
8. **Completion**: The use case ends successfully.

---

### 6. Alternate Flows

#### Alternate Flow 5a: Health Probe Failure / Service Unreachable (Downtime Alert)
- **5a1.** In Step 4, the microservice fails to respond within 3 seconds (timeout) or returns a non-200 HTTP response code (e.g., `500 Internal Server Error`, `503 Service Unavailable`).
- **5a2.** The system logs the probe failure and increments the consecutive failure counter for that microservice.
- **5a3.** If consecutive failures are less than 3, the system logs a `Warning` state and waits for the next 30-second interval cycle.
- **5a4.** If 3 consecutive failures occur, the system updates the microservice status to `Unhealthy` and logs an active downtime incident.
- **5a5.** The system invokes `«extend»` **UC-05: Send Downtime Alerts** to send notifications via Slack webhook and email to the assigned DevOps team.
- **5a6.** The system continues monitoring at 30-second intervals until the microservice responds with `HTTP 200 OK` on consecutive checks.
- **5a7.** Upon recovery, the system sets the status back to `Healthy`, records total downtime duration, dispatches a recovery alert, and resumes normal flow at Step 6.

#### Alternate Flow 3a: Invalid or Unreachable Health Endpoint Configuration
- **3a1.** In Step 3, the HTTP request fails due to DNS resolution failure or an invalid URL structure.
- **3a2.** The system flags the service entry with `Configuration Error` and logs the network error message.
- **3a3.** The system sends an administrative alert to the DevOps Engineer who registered the service to update the health endpoint configuration.
- **3a4.** The use case terminates for the affected service until registration details are corrected.
