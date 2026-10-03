# Local Development

This project is split into three deployable application components:

- `frontend`
- `task-service`
- `notification-service`

Keep platform work out of the application folders. The `devops/` directory is intentionally empty for now and should become the learning area for Docker Compose, Kubernetes, Helm, Argo CD, CI/CD, observability, and security assets.

## Suggested Startup Order

1. PostgreSQL
2. Redis
3. Kafka
4. `task-service`
5. `notification-service`
6. `frontend`

## Health And Metrics

Task service:

```bash
curl http://localhost:8080/actuator/health
curl http://localhost:8080/actuator/prometheus
```

Notification service:

```bash
curl http://localhost:8081/actuator/health
curl http://localhost:8081/actuator/prometheus
```

## API Examples

Create a task:

```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn probes","description":"Practice readiness and liveness probes"}'
```

List tasks:

```bash
curl http://localhost:8080/api/tasks
```

Complete a task:

```bash
curl -X PATCH http://localhost:8080/api/tasks/{taskId}/complete
```

