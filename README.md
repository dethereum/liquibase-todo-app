# Liquibase Todo App

A minimal full-stack todo list built with React (Vite), Node.js/Express, PostgreSQL, and Liquibase migrations.

## Prerequisites

- Node.js 18+
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
npm install
npm run dev
```

The API listens on `http://localhost:5000` by default and exposes:

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
server/                     Express API
  src/index.js              Routes/controllers
  src/db.js                 PostgreSQL pool helper
client/                     React UI
  src/App.jsx               Todo UI logic
```

## Next Steps

- Add authentication if you need multi-user lists
- Deploy the API + migrations via CI and point the React build to the deployed host
