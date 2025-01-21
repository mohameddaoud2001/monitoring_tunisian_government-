# Tunisian Government Project Monitoring API

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://your-build-system/build-status)  <!-- Replace with your actual build status badge -->
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) <!-- Replace with your license -->

## Overview

This project is a RESTful API and web application designed to enhance transparency and accountability in the management of Tunisian government projects. It serves as a digital dashboard connecting three key stakeholder groups:

*   **Government Officials:** Ministry and regional users can track project progress, manage budgets, update statuses, and handle deliverables.
*   **Citizens:** The public can access project information, monitor progress, view budget allocations, and provide feedback.
*   **Developers/Integrators:** The API allows developers to build civic tech applications, integrate with existing systems, and create innovative solutions using project data.

The system is bilingual (Arabic/English) and focuses on tracking:

*   Infrastructure projects
*   Budget allocation and expenses
*   Project deliverables
*   Public feedback
*   Regional development metrics

## Features

*   **RESTful API:** A well-structured API based on RESTful principles, providing endpoints for managing projects, regions, ministries, deliverables, expenses, and feedback.
*   **Authentication and Authorization:** Secure access control using JWT (JSON Web Tokens) and role-based permissions to ensure that users can only access and modify data relevant to their roles (citizen, ministry user, regional user).
*   **Bilingual Support:** Full Arabic and English language support for both the API and the web application.
*   **Project Tracking:** Detailed project information, including titles, descriptions, budgets, timelines, statuses, and progress updates.
*   **Regional Data:** Projects can be filtered and viewed by region (governorate) and ministry.
*   **Deliverables Management:** Track project milestones and deliverables with progress indicators.
*   **Public Feedback:** A system for citizens to submit feedback on projects, with sentiment analysis to gauge public opinion.
*   **Statistics and Reporting:** Generate reports and visualizations of project data, including budget utilization, project distribution by region/ministry, and feedback sentiment.
*   **Pagination, Filtering, and Sorting:** Efficiently handle large datasets with features for pagination, filtering, and sorting of project data.
*   **Web Application:** A user-friendly React-based frontend for easy access to project information and interaction with the API.
*   **Dockerized:** Containerized application using Docker and Docker Compose for easy deployment and development.

## Technology Stack

*   **Backend:**
    *   Python 3.10+
    *   Flask (Web Framework)
    *   Flask-SQLAlchemy (ORM)
    *   Flask-JWT-Extended (Authentication)
    *   Flask-Migrate (Database Migrations)
    *   Flask-CORS (Cross-Origin Resource Sharing)
    *   Flask-Smorest (API Framework)
    *   Marshmallow (Serialization/Deserialization)
    *   Gunicorn (WSGI HTTP Server)
    *   Psycopg2 (PostgreSQL Adapter)
*   **Database:**
    *   PostgreSQL
*   **Frontend:**
    *   React
    *   Material UI (Component Library)
    *   Axios (HTTP Client)
    *   Recharts (Charting Library)
    *   React Router (Routing)
*   **Containerization:**
    *   Docker
    *   Docker Compose

## Project Structure
content_copy
download
Use code with caution.
Markdown

![image](https://github.com/user-attachments/assets/657a1908-f2c7-4823-bbd0-f53ff87b66ad)


## Setup Instructions

### Prerequisites

*   Python 3.10+
*   pip
*   Node.js
*   npm
*   PostgreSQL
*   Git (optional)

### Local Development

1. **Clone the Repository (Optional):**

    ```bash
    git clone <repository_url>
    cd government-project-monitoring
    ```

2. **Backend Setup:**

    *   **Create a Virtual Environment:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```

    *   **Install Backend Dependencies:**

        ```bash
        pip install -r requirements.txt
        ```

    *   **Configure Environment Variables:**

        *   Create a `.env` file in the root directory:

            ```
            DATABASE_URL=postgresql://<your_db_user>:<your_db_password>@localhost/<your_db_name>
            SECRET_KEY=your_secret_key_here
            JWT_SECRET_KEY=your_jwt_secret_key_here
            ```

        *   Replace the placeholders with your actual database credentials and secret keys.

    *   **Initialize and Migrate the Database:**

        ```bash
        flask db upgrade
        ```

    *   **Create Initial Data (Optional):**

        ```bash
        python sample_data.py
        ```

    *   **Run the Flask Development Server:**

        ```bash
        python run.py
        ```

3. **Frontend Setup:**

    *   **Navigate to the Frontend Directory:**

        ```bash
        cd frontend
        ```

    *   **Install Frontend Dependencies:**

        ```bash
        npm install
        ```

![image](https://github.com/user-attachments/assets/2c958714-1e73-4928-afa5-e362b5ee6150)

![image](https://github.com/user-attachments/assets/77008ece-5da8-4a19-a4ab-664def71d40a)

    *   **Configure API Base URL (if needed):**

        *   Update `API_BASE_URL` in `frontend/src/config.js` if necessary.

    *   **Run the React Development Server:**

        ```bash
        npm start
        ```

### Docker Setup

1. **Build and Run using Docker Compose:**

    ```bash
    cd government-project-monitoring
    docker-compose build
    docker-compose up
    ```

## API Endpoints

| Method | Endpoint                       | Description                                                                  |
| :----- | :----------------------------- | :--------------------------------------------------------------------------- |
| POST   | `/api/v1/auth/register`        | Register a new user                                                          |
| POST   | `/api/v1/auth/login`           | Log in and obtain a JWT token                                                |
| GET    | `/api/v1/projects`             | Get a list of projects (with optional filtering, sorting, and pagination) |
| POST   | `/api/v1/projects`             | Create a new project                                                        |
| GET    | `/api/v1/projects/<project_id>` | Get details for a specific project                                          |
| PUT    | `/api/v1/projects/<project_id>` | Update a project                                                             |
| DELETE | `/api/v1/projects/<project_id>` | Delete a project                                                             |
| GET    | `/api/v1/regions`              | Get a list of regions                                                        |
| POST   | `/api/v1/regions`              | Create a new region                                                         |
| GET    | `/api/v1/ministries`           | Get a list of ministries                                                     |
| POST   | `/api/v1/ministries`           | Create a new ministry                                                        |
| GET    | `/api/v1/deliverables`         | Get a list of deliverables (for a project)                                   |
| POST   | `/api/v1/deliverables`         | Create a new deliverable                                                     |
| PUT    | `/api/v1/deliverables/<id>`    | Update a deliverable                                                          |
| DELETE | `/api/v1/deliverables/<id>`    | Delete a deliverable                                                          |
| GET    | `/api/v1/feedback`             | Get project feedback                                                         |
| POST   | `/api/v1/feedback`             | Submit feedback for a project                                                |
| GET    | `/api/v1/stats/projects`       | Get project statistics                                                       |
| GET    | `/api/v1/stats/feedback`       | Get feedback statistics                                                      |
| GET    | `/api/v1/expenses`             | Get a list of expenses (for a project)                                      |
| POST   | `/api/v1/expenses`             | Create a new expense                                                         |
| PUT    | `/api/v1/expenses/<id>`        | Update an expense                                                             |
| DELETE | `/api/v1/expenses/<id>`        | Delete an expense                                                             |


## Security

*   **Authentication:** JWT (JSON Web Tokens) are used for user authentication.
*   **Authorization:** Role-based access control (RBAC) restricts access to API endpoints based on user roles (e.g., `citizen`, `ministry_user`, `region_user`).
*   **Input Validation:** Marshmallow schemas are used to validate data received from API requests, preventing invalid or malicious data from entering the system.
*   **Rate Limiting:** The API implements rate limiting to prevent abuse and ensure fair usage.
*   **SQL Injection Prevention:** SQLAlchemy ORM is used to interact with the database, preventing SQL injection vulnerabilities.
*   **CORS:** Cross-Origin Resource Sharing (CORS) is configured to restrict API access to authorized origins (e.g., the frontend application).

## Testing


cd government-project-monitoring
pytest


##future improvement:

applying the INS  api (معهد الاحصاء الوطني) if they provide a comprehensive documentation on how to use their api as their website lacks guidance.
key value additions for integrating the Tunisia Data Portal API with this project :

1. Enriched Project Context: Access to 300+ national indicators provides deeper insights for project planning and impact assessment
2. Data-Driven Insights: Historical time series data helps set realistic targets and measure outcomes
3. Regional Analysis: Ability to compare project performance against regional development metrics

Implementation Overview:
```python
class TunisiaDataPortalService:
    # Handles API communication and XML data processing
    # Provides access to national indicators with monthly/annual granularity

class ProjectContextEnricher:
    # Enriches project data with relevant regional/national indicators
    # Links projects to broader economic and social context
```

Integration Points:
- New API endpoint for enriched project context
- Enhanced project dashboard with regional statistics
- Comparative visualizations showing project metrics vs. regional indicators


This integration would transform the system from a pure project monitoring tool into a comprehensive platform that connects individual projects to broader national development metrics, enabling better decision-making and impact assessment.
