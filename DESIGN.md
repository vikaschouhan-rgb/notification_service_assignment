# Notification Service - Design Document

## 🏗 High-Level Architecture

### Architecture Flow

1. Client sends notification request
2. API validates request
3. Notification is stored in database
4. Job is pushed to Redis queue
5. Worker processes notification asynchronously
6. Status is updated in database
7. Retry is triggered if failure occurs

### System Flow Diagram (Conceptual)

```
Client
   ↓
FastAPI (API Layer)
   ↓
Database (Store Notification)
   ↓
Redis Queue
   ↓
Worker(s)
   ↓
External Providers (Mocked)
   ↓
Update Status in DB
```

---

## 🗄 Database Schema

### 1. Notifications Table

| Field       | Description                    |
| ----------- | ------------------------------ |
| id          | Primary key                    |
| user_id     | User identifier                |
| message     | Notification content           |
| channel     | Email / SMS / Push             |
| priority    | high / medium / low |
| status      | pending / sent / failed        |
| retry_count | Number of retries attempted    |
| created_at  | Timestamp                      |
| updated_at  | Timestamp                      |

---

### 2. User Preferences Table

| Field      | Description      |
| ---------- | ---------------- |
| id         | Primary key      |
| user_id    | User identifier  |
| email      | Email preference |
| sms        | SMS preference   |
| push       | Push preference  |
| created_at | Timestamp        |

---

## 🔁 Failure Handling & Retry Strategy

The system uses an **exponential backoff retry mechanism** to handle failures.

### Retry Pattern

* Attempt 1 → after 10 seconds
* Attempt 2 → after 30 seconds
* Attempt 3 → after 60 seconds

If retries exceed the maximum limit:

* Notification status is marked as **`failed`**

### Benefits

* Improves reliability
* Handles temporary failures
* Prevents message loss

---

## 🔒 Reliability Design

The system ensures reliability using:

* Persistent queue (Redis)
* Retry mechanism with backoff
* Notification status tracking
* Database persistence

Even if a worker crashes:

* Jobs remain in Redis queue
* Processing resumes without data loss

---

## ⚡ Scalability Strategy

The system is designed to scale horizontally.

### Scaling Components

* Multiple FastAPI instances (behind load balancer)
* Multiple worker processes
* Redis as distributed queue
* Optimized database with indexing

### Example Scaling Architecture

```
        Load Balancer
              ↓
     -------------------
     |       |        |
   API1    API2     API3
     ↓        ↓        ↓
        Redis Queue Cluster
              ↓
     -------------------
     |       |        |
  Worker1  Worker2  Worker3
              ↓
         Database
```

---

## 📊 Observability

The system includes structured logging for monitoring and debugging.

### Logs Capture:

* Notification ID
* Channel
* Status (pending/sent/failed)
* Error messages
* Retry count

### Future Enhancements:

* Metrics collection (Prometheus)
* Dashboards (Grafana)
* Alerting system

---

## 🔑 Idempotency Design

To prevent duplicate notifications:

* Each request includes an **idempotency key**
* System checks if request already exists:

  * If yes → return previous response
  * If no → process normally

### Benefits:

* Prevents duplicate notifications
* Ensures safe retries
* Improves API reliability

---

## ⚖️ Trade-offs & Design Decisions

### 1. Redis + RQ instead of Kafka

**Why chosen:**

* Simple setup
* Faster development
* Suitable for assignment scope
* Low operational complexity

**Trade-off:**

* Less scalable than Kafka
* But sufficient for demonstration

---

### 2. PostgreSQL instead of NoSQL

**Why chosen:**

* Strong consistency
* Structured schema
* Easy querying

**Trade-off:**

* Requires schema migrations
* Less flexible than NoSQL

---

### 3. Mock Providers instead of Real Integrations

**Why chosen:**

* Focus on system design
* Avoid external dependency failures
* Faster development and testing

---

## 🚀 Future Improvements

* Dead Letter Queue (DLQ)
* Rate limiting per user
* Webhook support for delivery updates
* Analytics dashboard
* Circuit breaker pattern for external services
* Docker & Kubernetes deployment

---

## 📌 Conclusion

This Notification Service demonstrates production-grade backend design principles:

* Asynchronous processing using queues
* Reliable retry mechanisms
* Scalable architecture
* Clean separation of concerns

The system is designed to be **extensible, reliable, and scalable**, while keeping the implementation simple and easy to understand.
