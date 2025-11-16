# Liquibase Todo App

A minimal full-stack todo list built with React (Vite), FastAPI, PostgreSQL, and Liquibase migrations.

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Liquibase CLI (and PostgreSQL JDBC driver jar)

## Database & Liquibase

0. Download class driver curl -L https://jdbc.postgresql.org/download/postgresql-42.7.3.jar -o liquibase/drivers/postgresql-42.7.3.jar
1. Create a database (default name `todo_app`).
2. Update `liquibase/liquibase.properties` or copy it to `liquibase/liquibase.local.properties` and edit credentials / classpath.
3. Run the migrations:

   ```bash
   cd liquibase
   liquibase --defaultsFile=liquibase.local.properties update
   ```

   If you keep the defaults, you can omit `--defaultsFile` and Liquibase will pick up `liquibase.properties`.

The initial changelog creates the `todos` table with `id`, `title`, `is_complete`, and `created_at` columns plus an index on `created_at`.

## API (server)

```bash
cd server
cp .env.example .env   # adjust DATABASE_URL / PORT if needed
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The FastAPI server listens on `http://localhost:5000` by default and exposes:

- `GET /api/todos` — list todos (newest first)
- `POST /api/todos` — create `{ "title": string }`
- `PATCH /api/todos/:id` — toggle completion `{ "isComplete": boolean }`
- `DELETE /api/todos/:id` — remove a todo
- `GET /api/health` — connectivity check

## Client (React)

```bash
cd client
cp .env.example .env   # optional override for Vite env vars
npm install
npm run dev
```

The Vite dev server runs on `http://localhost:5173` and proxies `/api` to the backend so both apps can talk without extra configuration. Set `VITE_API_BASE_URL` if you deploy the API elsewhere.

## Project Structure

```
liquibase/                  Liquibase changelog + properties
server/                     FastAPI service
  app.py                    Core API + DB access
  main.py                   Local development entrypoint (uvicorn)
  lambda_handler.py         AWS Lambda adapter via Mangum
client/                     React UI
  src/App.jsx               Todo UI logic
```

## Next Steps

- Add authentication if you need multi-user lists
- Deploy the API + migrations via CI and point the React build to the deployed host
