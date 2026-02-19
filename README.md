# Travel Application

A full-stack travel booking application built to demonstrate the implementation of the Application Layer. This project features a robust RESTful API, a relational database, session-based authentication, a command-line interface (CLI), and containerization for cloud deployment.

## Features

- **RESTful API**: Built with Flask and Connexion using the OpenAPI (Swagger) specification.
- **Relational Database**: SQLite integration for managing users, bookings, and destinations.
- **Authentication**: Secure session-based login system with password hashing.
- **User Interface**: Flask-based frontend for interacting with the API.
- **Command Line Interface (CLI)**: Built with `argparse` for terminal-based interactions.
- **Containerization**: Dockerized application (split into API and Frontend containers).
- **Architecture**: Designed and documented using the C4 Model.

---

## Architecture (C4 Model)

The system architecture is documented using the C4 model to visualize the context, containers, and components.

- **Context Diagram**: Shows how the Travel Application fits in with user interactions and external systems.
- **Container Diagram**: Highlights the separation between the Frontend (Flask), API (Connexion), and Database (SQLite).
- **Component Diagram**: details the internal logic of the API and Database layers.

*See the docs/c4-model.pdf or equivalent in the repository for detailed diagrams.*

---

## Prerequisites

- **Python 3.8+**
- **Docker** (for containerized deployment)
- **Azure CLI** (optional, for Azure Container Instances deployment)

---

## Installation & Setup (Local Development)

Follow these steps to run the application on your local machine using a Python Virtual Environment.

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```
### 2. Create and Activate Virtual Environment
```bash
Copy code
py -m venv .venv
.\.venv\Scripts\activate
```
### 3. Install Dependencies
```bash
Copy code
pip install -r requirements.txt
```
### 4. Initialize the Database
Before running the application for the first time, you must initialize the SQLite database.
```bash
Copy code
python create_db.py 
```
## Running the Application
You can run the components separately.
Assuming a standard setup where the frontend proxies API requests:

### 1. Start the API Server:
```bash
python travel_api.py
```
The API will typically run at http://localhost:82. 
The Swagger UI (OpenAPI documentation) is usually available at http://localhost:82/ui.

### 2. Start the Frontend (in a new terminal):

```bash
python frontend_api.py
```
Access the website at http://localhost:80.

## Docker Deployment
The application is containerized using Docker. It consists of two containers: one for the API and one for the Frontend.

### 1. Build and Run Locally
```bash
Copy code
docker-compose up --build
```
This will start both the API and Frontend containers. Access the frontend at http://localhost:80 (or configured port).

### 2. Deploy to Azure (Container Instances)
The application has been pushed to Azure Container Registry (ACR) and deployed to Azure Container Instances (ACI) for public access.

Note: To redeploy, ensure you are logged in to Azure and use the Azure CLI or the Azure Portal to run the containers defined in your docker-compose.yml.

## 📖 API Documentation
Since this project uses Connexion and OpenAPI, interactive API documentation is automatically generated.

Run the application.
Navigate to the Swagger UI (usually http://localhost:82/ui) to test endpoints, view schemas, and authenticate.
