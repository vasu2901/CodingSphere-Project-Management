# 🛠️ Project Management API – FastAPI

This is a **FastAPI-based RESTful API** assessment for CodingSphere. It supports user and admin authentication and allows creating, updating, deleting, and retrieving projects with role-based access control using JWT authentication.

---

## 📦 Features

* **User Authentication**

  * User Signup
  * Admin Signup
  * Login with JWT
* **Project Management**

  * Create a Project (`POST`)
  * Get All Projects (`GET`)
  * Update a Project (`PUT`)
  * Delete a Project (`DELETE`)
* **Role-Based Access Control (RBAC)**

  * Admins can create, update, and delete projects.
  * Users can only view projects in which they are members.

---

## 🔗 API Endpoints

| Method   | Endpoint         | Description              | Auth Required  |
| -------- | ---------------- | ------------------------ | -------------- |
| `POST`   | `/auth/register`   | Register as a user       | ❌              |
| `POST`   | `/auth/adminRegister`  | Register as an admin     | ❌              |
| `POST`   | `/login`         | Login and get JWT token  | ❌              |
| `POST`   | `/projects/`     | Create a new project     | ✅ (Admin only) |
| `GET`    | `/projects/`     | Get all related projects | ✅              |
| `PUT`    | `/projects/{id}` | Update a project         | ✅ (Admin only) |
| `DELETE` | `/projects/{id}` | Delete a project         | ✅ (Admin only) |

---

## Dependencies

### 1. Python

### 2. PostgreSQL URL.

## 🚀 Quick Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/vasu2901/CodingSphere-Project-Management.git
cd CodingSphere-Project-Management
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your environment variables


### 5. Start the Server

```bash
uvicorn main:app --reload
```

---

## 🔐 Authentication

After logging in with `/login`, you'll receive a JWT token:

```
{
  "access_token": "<your-token>",
  "token_type": "bearer",
  "expired_At": "2025-08-02T10:24:19.418Z"
}
```

Use this token in the `Authorization` header for protected endpoints:

```
Authorization: Bearer <your-token>
```

---

## 🧪 API Usage

### User Signup
```http
POST /auth/register

{
  "username": "",
  "password": "",
}
```

### Admin Signup
```http
POST /auth/adminRegister

{
  "username": "",
  "password": "",
}
```

### Login
```http
POST /auth/login

{
  "username": "",
  "password": "",
}
```

### Get Projects

```http
GET /projects/
Authorization: Bearer <admin-token>
Content-Type: application/json
```

### Create Project (Admin Only)

```http
POST /projects/
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "title": "New Project",
  "description": "Sample project for testing",
  "member": [2,4,5] # List of user Ids
}
```


### Update Project (Admin Only)

```http
PUT /projects/{project_id}
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "title": "New Project",
  "description": "Sample project for testing",
  "member": [2,4,5] # List of user Ids
}
```

### DELETE Project (Admin Only)

```http
DELETE /projects/{project_id}
Authorization: Bearer <admin-token>
Content-Type: application/json
```

### 📽️ Demo Video

Watch the project in action:  
🔗 [Click here to view the demo on Loom](https://www.loom.com/share/2d7a4ac18de44160b4af8b9b9e604103?sid=a370d4d0-6bae-4857-9e8c-e1dd081f8606)

---

