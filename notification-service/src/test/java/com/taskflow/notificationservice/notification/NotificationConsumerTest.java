package com.taskflow.notificationservice.notification;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class NotificationConsumerTest {
    private final NotificationRepository repository = mock(NotificationRepository.class);
    private final Clock clock = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
    private final NotificationConsumer consumer = new NotificationConsumer(repository, clock);

    @Test
    void recordsConsumedTaskEvent() {
        when(repository.save(any(NotificationRecord.class))).thenAnswer(invocation -> invocation.getArgument(0));
        TaskEvent event = new TaskEvent(UUID.randomUUID(), "TASK_CREATED", "Learn Helm", Instant.now(clock));

        consumer.consume(event);

        verify(repository).save(any(NotificationRecord.class));
    }

    @Test
    void createsProcessedNotificationRecord() {
        NotificationRecord record = new NotificationRecord(
                UUID.randomUUID(),
                UUID.randomUUID(),
                "TASK_COMPLETED",
                NotificationStatus.PROCESSED,
                "Processed TASK_COMPLETED",
                Instant.now(clock)
        );

        assertThat(record.getStatus()).isEqualTo(NotificationStatus.PROCESSED);
    }
}

