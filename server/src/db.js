const { Pool } = require('pg');

const { DATABASE_URL, PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD, NODE_ENV } = process.env;

const pool = new Pool(
  DATABASE_URL
    ? {
        connectionString: DATABASE_URL,
        ssl:
          NODE_ENV === 'production'
            ? { rejectUnauthorized: false }
            : false,
      }
    : {
        host: PGHOST || 'localhost',
        port: PGPORT ? Number(PGPORT) : 5432,
        database: PGDATABASE || 'todo_app',
        user: PGUSER || 'postgres',
        password: PGPASSWORD || 'postgres',
      }
);

pool.on('error', (error) => {
  console.error('Unexpected Postgres error', error);
  process.exit(1);
});

module.exports = {
  query: (text, params) => pool.query(text, params),
  pool,
};
