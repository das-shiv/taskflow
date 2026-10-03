package com.taskflow.notificationservice.notification;

import java.time.Clock;
import java.time.Instant;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class NotificationConsumer {
    private static final Logger log = LoggerFactory.getLogger(NotificationConsumer.class);

    private final NotificationRepository repository;
    private final Clock clock;

    public NotificationConsumer(NotificationRepository repository, Clock clock) {
        this.repository = repository;
        this.clock = clock;
    }

    @KafkaListener(topics = "${taskflow.kafka.task-events-topic}")
    public void consume(TaskEvent event) {
        Instant receivedAt = Instant.now(clock);
        String message = "Processed %s for task %s".formatted(event.eventType(), event.taskId());
        NotificationRecord record = new NotificationRecord(
                UUID.randomUUID(),
                event.taskId(),
                event.eventType(),
                NotificationStatus.PROCESSED,
                message,
                receivedAt
        );
        repository.save(record);
        log.info("task notification processed taskId={} eventType={}", event.taskId(), event.eventType());
    }
}

