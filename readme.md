
Here’s an updated version of the README with **Kong** integration mentioned:

---

# MartAPI

MartAPI is a robust and scalable marketplace API built with FastAPI. It provides core functionalities like user management, product listings, and secure transactions using JWT authentication. The project leverages **Docker Compose** for containerization and **Kong API Gateway** for managing, securing, and routing API requests.

## Features

- FastAPI for high-performance API functionality.
- JWT-based authentication for secure, stateless user sessions.
- SQLAlchemy ORM for seamless database management.
- Docker Compose for easy setup and containerized deployment.
- Kong API Gateway for managing API requests, load balancing, and security.

## Tech Stack

- **FastAPI**: Modern, fast web framework for Python APIs.
- **SQLAlchemy**: ORM for handling database interactions.
- **JWT**: Secure user authentication.
- **Docker**: Containerization for consistent development and deployment environments.
- **Kong**: API Gateway for managing and securing API traffic.

## Installation

### Prerequisites

- Docker
- Docker Compose
- Kong (for API Gateway)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/muneebxhasan/martapi.git
   cd martapi
   ```

2. Create a `.env` file with the following content:
   ```
   SECRET_KEY=your_jwt_secret_key
   DATABASE_URL=postgresql://postgres:postgres@db/martapi_db
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. Run the following command to build and start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```



4. Now, you can access the API through Kong at `http://localhost:8000/`.

## Environment Variables

- `SECRET_KEY`: Your JWT secret key.
- `DATABASE_URL`: The URL for the database (e.g., PostgreSQL).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes.

## API Endpoints

### Authentication

- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Login and retrieve a JWT token.

### User Management

- `GET /users/me`: Retrieve user details.
- `PUT /users/me`: Update user information.



## License

This project is licensed under the MIT License.

---

This version includes **Kong** integration for API management. Let me know if it fits your requirements!
