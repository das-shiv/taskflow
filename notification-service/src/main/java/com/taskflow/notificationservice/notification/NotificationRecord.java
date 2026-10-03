package com.taskflow.notificationservice.notification;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "notifications")
public class NotificationRecord {
    @Id
    private UUID id;

    @Column(nullable = false)
    private UUID taskId;

    @Column(nullable = false, length = 64)
    private String eventType;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 32)
    private NotificationStatus status;

    @Column(nullable = false, length = 512)
    private String message;

    @Column(nullable = false)
    private Instant receivedAt;

    protected NotificationRecord() {
    }

    public NotificationRecord(UUID id, UUID taskId, String eventType, NotificationStatus status, String message, Instant receivedAt) {
        this.id = id;
        this.taskId = taskId;
        this.eventType = eventType;
        this.status = status;
        this.message = message;
        this.receivedAt = receivedAt;
    }

    public UUID getId() {
        return id;
    }

    public UUID getTaskId() {
        return taskId;
    }

    public String getEventType() {
        return eventType;
    }

    public NotificationStatus getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }

    public Instant getReceivedAt() {
        return receivedAt;
    }
}

