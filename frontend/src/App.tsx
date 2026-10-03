import { FormEvent, useEffect, useState } from 'react';
import { CheckCircle2, Loader2, Plus } from 'lucide-react';
import { completeTask, createTask, listTasks, Task } from './api';

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    setError(null);
    setLoading(true);
    try {
      setTasks(await listTasks());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void refresh();
  }, []);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!title.trim()) {
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const task = await createTask(title.trim(), description.trim());
      setTasks((current) => [task, ...current]);
      setTitle('');
      setDescription('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error');
    } finally {
      setSaving(false);
    }
  }

  async function onComplete(id: string) {
    setError(null);
    try {
      const updated = await completeTask(id);
      setTasks((current) => current.map((task) => (task.id === id ? updated : task)));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error');
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <header className="page-header">
          <div>
            <p className="eyebrow">DevOps practice app</p>
            <h1>TaskFlow</h1>
          </div>
          <button className="secondary" onClick={() => void refresh()} disabled={loading}>
            {loading ? <Loader2 className="spin" size={18} /> : 'Refresh'}
          </button>
        </header>

        <form className="task-form" onSubmit={onSubmit}>
          <input
            aria-label="Task title"
            placeholder="Task title"
            value={title}
            maxLength={140}
            onChange={(event) => setTitle(event.target.value)}
          />
          <input
            aria-label="Task description"
            placeholder="Description"
            value={description}
            maxLength={1000}
            onChange={(event) => setDescription(event.target.value)}
          />
          <button type="submit" disabled={saving || !title.trim()} aria-label="Create task">
            {saving ? <Loader2 className="spin" size={18} /> : <Plus size={18} />}
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        <section className="task-list" aria-live="polite">
          {loading ? (
            <p className="muted">Loading tasks...</p>
          ) : tasks.length === 0 ? (
            <p className="muted">No tasks yet.</p>
          ) : (
            tasks.map((task) => (
              <article className="task-card" key={task.id}>
                <div>
                  <h2>{task.title}</h2>
                  {task.description && <p>{task.description}</p>}
                  <span className={task.status === 'COMPLETED' ? 'status complete' : 'status'}>
                    {task.status}
                  </span>
                </div>
                <button
                  className="icon-button"
                  onClick={() => void onComplete(task.id)}
                  disabled={task.status === 'COMPLETED'}
                  aria-label={`Complete ${task.title}`}
                >
                  <CheckCircle2 size={20} />
                </button>
              </article>
            ))
          )}
        </section>
      </section>
    </main>
  );
}

