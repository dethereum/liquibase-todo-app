const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

async function handleResponse(response) {
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || 'Request failed');
  }
  if (response.status === 204) return null;
  return response.json();
}

export const fetchTodos = () => fetch(`${API_BASE_URL}/todos`).then(handleResponse);

export const createTodo = (title) =>
  fetch(`${API_BASE_URL}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  }).then(handleResponse);

export const updateTodo = (id, payload) =>
  fetch(`${API_BASE_URL}/todos/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }).then(handleResponse);

export const deleteTodo = (id) =>
  fetch(`${API_BASE_URL}/todos/${id}`, { method: 'DELETE' }).then(handleResponse);
