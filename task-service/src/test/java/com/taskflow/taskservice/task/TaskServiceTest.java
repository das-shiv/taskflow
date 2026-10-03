package com.taskflow.taskservice.task;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.kafka.core.KafkaTemplate;

class TaskServiceTest {
    private final TaskRepository repository = mock(TaskRepository.class);
    private final KafkaTemplate<String, TaskEvent> kafkaTemplate = mock(KafkaTemplate.class);
    private final Clock clock = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
    private final TaskService service = new TaskService(repository, kafkaTemplate, "task-events", clock);

    @Test
    void createsTaskAndPublishesEvent() {
        when(repository.save(any(Task.class))).thenAnswer(invocation -> invocation.getArgument(0));

        TaskResponse response = service.create(new CreateTaskRequest("Learn Kubernetes", "Deploy a pod"));

        assertThat(response.title()).isEqualTo("Learn Kubernetes");
        assertThat(response.status()).isEqualTo(TaskStatus.OPEN);
        verify(kafkaTemplate).send(eq("task-events"), eq(response.id().toString()), any(TaskEvent.class));
    }

    @Test
    void completesTaskAndPublishesEvent() {
        UUID taskId = UUID.randomUUID();
        Task task = new Task(taskId, "Learn rollback", null, Instant.parse("2026-01-01T00:00:00Z"));
        when(repository.findById(taskId)).thenReturn(Optional.of(task));

        TaskResponse response = service.complete(taskId);

        assertThat(response.status()).isEqualTo(TaskStatus.COMPLETED);
        assertThat(response.completedAt()).isEqualTo(Instant.parse("2026-01-01T00:00:00Z"));
        verify(kafkaTemplate).send(eq("task-events"), eq(taskId.toString()), any(TaskEvent.class));
    }

    @Test
    void listsTasks() {
        Task task = new Task(UUID.randomUUID(), "Read events", "Check Kafka", Instant.now(clock));
        when(repository.findAll()).thenReturn(List.of(task));

        assertThat(service.list()).hasSize(1);
    }
}

