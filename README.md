# TaskFlow

TaskFlow is a small task-management application built as the application layer for a DevOps and Kubernetes learning project.

The business domain is intentionally small:

- React frontend for listing, creating, and completing tasks.
- `task-service` Spring Boot API with PostgreSQL persistence, Flyway migrations, Redis caching, Kafka task events, Actuator, and Prometheus metrics.
- `notification-service` Spring Boot Kafka consumer that records processed task notifications.

The `devops/` folder is intentionally empty. It is reserved for learning and will later hold Kubernetes, Helm, Argo CD, CI/CD, observability, security, and scripting assets.

## Repository Layout

```text
taskflow/
  frontend/
  task-service/
  notification-service/
  database/
    migrations/
  devops/
  docs/
  README.md
```

## Prerequisites

- Node.js 20+
- Java 21
- Maven 3.9+
- PostgreSQL 15+
- Redis 7+
- Kafka 3+

## Local Environment

`task-service` uses these environment variables:

```text
SERVER_PORT=8080
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/taskflow
SPRING_DATASOURCE_USERNAME=taskflow
SPRING_DATASOURCE_PASSWORD=taskflow
SPRING_DATA_REDIS_HOST=localhost
SPRING_DATA_REDIS_PORT=6379
SPRING_KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TASKFLOW_KAFKA_TASK_EVENTS_TOPIC=task-events
```

`notification-service` uses these environment variables:

```text
SERVER_PORT=8081
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/taskflow_notifications
SPRING_DATASOURCE_USERNAME=taskflow
SPRING_DATASOURCE_PASSWORD=taskflow
SPRING_KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TASKFLOW_KAFKA_TASK_EVENTS_TOPIC=task-events
```

`frontend` uses:

```text
VITE_TASK_API_BASE_URL=http://localhost:8080
```

## Run Locally

Start the API:

```bash
cd task-service
mvn spring-boot:run
```

Start the notification consumer:

```bash
cd notification-service
mvn spring-boot:run
```

Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

## Tests

```bash
cd task-service
mvn test

cd ../notification-service
mvn test

cd ../frontend
npm test
```

## Container Images

Each application component includes a Dockerfile:

- `frontend/Dockerfile`
- `task-service/Dockerfile`
- `notification-service/Dockerfile`

The runtime stages use non-root users and are ready for later Kubernetes deployment work.

