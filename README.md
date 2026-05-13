# 📚 Library Service API (Django REST Framework)

A RESTful API for managing a library system, including books, users, and borrowings.  
The project is built with Django and Django REST Framework and uses JWT authentication for secure access.

---

## Features

- Book management (CRUD with inventory tracking)
- Custom user model with email authentication
- JWT authentication (access & refresh tokens)
- Borrowing system (issue and return books)
- Filtering borrowings by active status and user
- Role-based permissions (admin vs regular users)
- Swagger/OpenAPI documentation

---

## Project Structure

- **Users app** – custom user model and authentication
- **Books app** – book catalog with inventory and pricing
- **Borrowings app** – book issuing and return tracking

---

## Authentication

This project uses JWT authentication.

## Example Workflow

1. Register user
2. Obtain JWT token
3. Create borrowing
4. Return book
5. Track inventory changes automatically

## Run with Docker
```bash
docker-compose build
docker-compose up
