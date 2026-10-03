export type TaskStatus = 'OPEN' | 'COMPLETED';

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
}

const baseUrl = import.meta.env.VITE_TASK_API_BASE_URL ?? 'http://localhost:8080';

export async function listTasks(): Promise<Task[]> {
  const response = await fetch(`${baseUrl}/api/tasks`);
  if (!response.ok) {
    throw new Error('Unable to load tasks');
  }
  return response.json();
}

export async function createTask(title: string, description: string): Promise<Task> {
  const response = await fetch(`${baseUrl}/api/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description }),
  });
  if (!response.ok) {
    throw new Error('Unable to create task');
  }
  return response.json();
}

export async function completeTask(id: string): Promise<Task> {
  const response = await fetch(`${baseUrl}/api/tasks/${id}/complete`, {
    method: 'PATCH',
  });
  if (!response.ok) {
    throw new Error('Unable to complete task');
  }
  return response.json();
}

