package com.taskflow.taskservice.task;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CreateTaskRequest(
        @NotBlank @Size(max = 140) String title,
        @Size(max = 1000) String description
) {
}

