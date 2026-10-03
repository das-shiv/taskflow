package com.taskflow.taskservice.task;

import java.time.Clock;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TaskService {
    private final TaskRepository repository;
    private final KafkaTemplate<String, TaskEvent> kafkaTemplate;
    private final String topic;
    private final Clock clock;

    public TaskService(
            TaskRepository repository,
            KafkaTemplate<String, TaskEvent> kafkaTemplate,
            @Value("${taskflow.kafka.task-events-topic}") String topic,
            Clock clock
    ) {
        this.repository = repository;
        this.kafkaTemplate = kafkaTemplate;
        this.topic = topic;
        this.clock = clock;
    }

    @Cacheable("tasks")
    @Transactional(readOnly = true)
    public List<TaskResponse> list() {
        return repository.findAll().stream().map(TaskResponse::from).toList();
    }

    @CacheEvict(value = "tasks", allEntries = true)
    @Transactional
    public TaskResponse create(CreateTaskRequest request) {
        Instant now = Instant.now(clock);
        Task task = repository.save(new Task(UUID.randomUUID(), request.title(), request.description(), now));
        publish(task, "TASK_CREATED", now);
        return TaskResponse.from(task);
    }

    @CacheEvict(value = "tasks", allEntries = true)
    @Transactional
    public TaskResponse complete(UUID id) {
        Task task = repository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
        Instant now = Instant.now(clock);
        task.complete(now);
        publish(task, "TASK_COMPLETED", now);
        return TaskResponse.from(task);
    }

    private void publish(Task task, String eventType, Instant occurredAt) {
        TaskEvent event = new TaskEvent(task.getId(), eventType, task.getTitle(), occurredAt);
        kafkaTemplate.send(topic, task.getId().toString(), event);
    }
}

