# HXNID-Bot-WA

This project consists of two main services: a Go-based WhatsApp API and a Python-based WhatsApp bot, orchestrated using Docker Compose.

## Prerequisites

Before running this project, ensure you have the following installed:

*   **Docker**: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
*   **Docker Compose**: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Setup

1.  **Environment Variables**:
    Create a `.env` file in the root directory of the project by copying the `.env.example` file.

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file and configure the necessary environment variables for both the Go API and the Python bot.

## Running the Application with Docker Compose

To build and run both services using Docker Compose, navigate to the root directory of the project (where `docker-compose.yml` is located) and execute the following command:

```bash
docker-compose up --build -d
```

*   `up`: Starts the services defined in `docker-compose.yml`.
*   `--build`: Builds the Docker images for the services before starting them. This is important for the first run or after any changes to the Dockerfiles or application code.
*   `-d`: Runs the containers in detached mode (in the background).

This command will:
1.  Build the Docker image for the `whatsapp_go` service.
2.  Build the Docker image for the `whatsapp_python` service.
3.  Start both services, making them accessible on their respective ports (3000 for Go API, 5000 for Python bot) as defined in `docker-compose.yml`.

## Stopping the Application

To stop and remove the running containers, networks, and volumes created by `docker-compose up`, run the following command from the project root directory:

```bash
docker-compose down
```

## Accessing Services

*   **Go WhatsApp API**: Accessible at `http://localhost:3000`
*   **Python WhatsApp Bot**: Accessible at `http://localhost:5000` (This service depends on the Go API)
