import { useEffect, useState } from 'react';
import { createTodo, deleteTodo, fetchTodos, updateTodo } from './api.js';

export default function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newTitle, setNewTitle] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [mutatingId, setMutatingId] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchTodos();
        setTodos(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!newTitle.trim()) return;

    try {
      setSubmitting(true);
      const todo = await createTodo(newTitle.trim());
      setTodos((prev) => [todo, ...prev]);
      setNewTitle('');
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const toggleComplete = async (todo) => {
    try {
      setMutatingId(todo.id);
      const updated = await updateTodo(todo.id, { isComplete: !todo.isComplete });
      setTodos((prev) => prev.map((t) => (t.id === todo.id ? updated : t)));
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setMutatingId(null);
    }
  };

  const handleDelete = async (todo) => {
    if (!confirm(`Delete "${todo.title}"?`)) return;

    try {
      setMutatingId(todo.id);
      await deleteTodo(todo.id);
      setTodos((prev) => prev.filter((t) => t.id !== todo.id));
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setMutatingId(null);
    }
  };

  return (
    <div className="app-shell">
      <h1>Todos</h1>
      <form className="todo-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Add a task"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          disabled={submitting}
        />
        <button disabled={submitting || !newTitle.trim()} type="submit">
          Add
        </button>
      </form>

      {error && (
        <p className="empty-state" role="alert">
          {error}
        </p>
      )}

      {loading ? (
        <p className="empty-state">Loading…</p>
      ) : todos.length === 0 ? (
        <p className="empty-state">No todos yet. Create your first task!</p>
      ) : (
        <ul className="todo-list">
          {todos.map((todo) => (
            <li key={todo.id} className="todo-item">
              <div className="todo-left">
                <input
                  type="checkbox"
                  checked={todo.isComplete}
                  disabled={mutatingId === todo.id}
                  onChange={() => toggleComplete(todo)}
                />
                <p className={`todo-title ${todo.isComplete ? 'complete' : ''}`}>
                  {todo.title}
                </p>
              </div>
              <button
                className="delete-btn"
                onClick={() => handleDelete(todo)}
                disabled={mutatingId === todo.id}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
