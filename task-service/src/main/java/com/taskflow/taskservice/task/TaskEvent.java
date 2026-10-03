package com.taskflow.taskservice.task;

import java.time.Instant;
import java.util.UUID;

public record TaskEvent(
        UUID taskId,
        String eventType,
        String title,
        Instant occurredAt
) {
}

