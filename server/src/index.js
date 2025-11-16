require('dotenv').config();
const express = require('express');
const cors = require('cors');
const db = require('./db');

const PORT = process.env.PORT || 5000;
const CLIENT_ORIGIN = process.env.CLIENT_ORIGIN || '*';

const app = express();
app.use(cors({ origin: CLIENT_ORIGIN }));
app.use(express.json());

const mapTodo = (row) => ({
  id: row.id,
  title: row.title,
  isComplete: row.is_complete,
  createdAt: row.created_at,
});

app.get('/api/health', async (req, res, next) => {
  try {
    await db.query('SELECT 1');
    res.json({ ok: true });
  } catch (error) {
    next(error);
  }
});

app.get('/api/todos', async (req, res, next) => {
  try {
    const { rows } = await db.query(
      'SELECT id, title, is_complete, created_at FROM todos ORDER BY created_at DESC'
    );
    res.json(rows.map(mapTodo));
  } catch (error) {
    next(error);
  }
});

app.post('/api/todos', async (req, res, next) => {
  try {
    const { title } = req.body;
    if (typeof title !== 'string' || title.trim().length === 0) {
      return res.status(400).json({ message: 'title is required' });
    }

    const { rows } = await db.query(
      'INSERT INTO todos (title) VALUES ($1) RETURNING id, title, is_complete, created_at',
      [title.trim()]
    );

    res.status(201).json(mapTodo(rows[0]));
  } catch (error) {
    next(error);
  }
});

app.patch('/api/todos/:id', async (req, res, next) => {
  try {
    const { id } = req.params;
    const todoId = Number(id);
    const { isComplete } = req.body;

    if (!Number.isInteger(todoId)) {
      return res.status(400).json({ message: 'Invalid id parameter' });
    }

    if (typeof isComplete !== 'boolean') {
      return res.status(400).json({ message: 'isComplete must be boolean' });
    }

    const { rows } = await db.query(
      'UPDATE todos SET is_complete = $1 WHERE id = $2 RETURNING id, title, is_complete, created_at',
      [isComplete, todoId]
    );

    if (!rows.length) {
      return res.status(404).json({ message: 'Todo not found' });
    }

    res.json(mapTodo(rows[0]));
  } catch (error) {
    next(error);
  }
});

app.delete('/api/todos/:id', async (req, res, next) => {
  try {
    const { id } = req.params;
    const todoId = Number(id);

    if (!Number.isInteger(todoId)) {
      return res.status(400).json({ message: 'Invalid id parameter' });
    }

    const { rowCount } = await db.query('DELETE FROM todos WHERE id = $1', [todoId]);

    if (!rowCount) {
      return res.status(404).json({ message: 'Todo not found' });
    }

    res.status(204).send();
  } catch (error) {
    next(error);
  }
});

// basic error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ message: 'Unexpected error' });
});

app.listen(PORT, () => {
  console.log(`API listening on http://localhost:${PORT}`);
});
