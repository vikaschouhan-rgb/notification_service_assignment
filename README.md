# Notification Service

## 🚀 Project Overview

This is a backend Notification Service built using FastAPI that supports sending notifications to users across multiple channels such as Email, SMS, and Push.

The service is designed to be scalable, reliable, and extensible, acting as a centralized system for handling all user communications.

---

## ✨ Features

* Multi-channel notification support (Email, SMS, Push)
* User preference management (opt-in / opt-out)
* Notification priority handling (critical, high, normal, low)
* Notification delivery tracking (pending, sent, failed)
* RESTful APIs for managing notifications and preferences
* Clean architecture with separation of concerns

---

## 🛠 Tech Stack

| Technology          | Purpose                         |
| ------------------- | ------------------------------- |
| FastAPI             | Web framework for building APIs |
| SQLAlchemy          | ORM for database interaction    |
| PostgreSQL / SQLite | Database                        |
| Pydantic            | Data validation                 |
| Uvicorn             | ASGI server                     |

### Why FastAPI?

* High performance with async support
* Built-in Swagger UI for API testing
* Easy request/response validation

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd notification-service
```

### 2. Create virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

### 5. Access API Docs

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### 🔔 Notifications

| Method | Endpoint                       | Description             |
| ------ | ------------------------------ | ----------------------- |
| POST   | /notifications                 | Create a notification   |
| GET    | /notifications                 | Get all notifications   |
| GET    | /notifications/{id}            | Get notification status |
| GET    | /users/{user_id}/notifications | Get user notifications  |

---

### 👤 User Preferences

| Method | Endpoint                     | Description               |
| ------ | ---------------------------- | ------------------------- |
| POST   | /users/{user_id}/preferences | Create/Update preferences |
| GET    | /users/{user_id}/preferences | Get user preferences      |

---

## 📦 Sample Request

### Create Notification

```json
POST /notifications
{
  "user_id": 1,
  "channel": "email",
  "message": "Hello User!",
  "priority": "high",
  "recipient": "user@example.com"
}
```

---

## 🧪 Running Tests

```bash
pytest
```

> Make sure you have a `/tests` folder with test cases.

---

## ⚠️ Assumptions

* Authentication is handled externally (API Gateway)
* User service is separate; only `user_id` is stored
* Email/SMS/Push providers are mocked (no real integration)
* Notifications are processed synchronously (no queue yet)
* Templates are not implemented (can be added later)

---

## 🚧 Future Improvements

* Add message queue (Redis / RabbitMQ)
* Implement retry mechanism with exponential backoff
* Add rate limiting per user
* Add template engine with variable substitution
* Add async background processing
* Add webhook support for delivery status

---

## 📄 API Documentation

Swagger UI available at:

```
http://127.0.0.1:8000/docs
```

---

