const express = require('express');
const pg = require('pg');
const path = require('path');

try {
  process.loadEnvFile();
} catch {
  console.warn('setup an .env file');
}

const pool = new pg.Pool({
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  database: process.env.POSTGRES_DB,
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
});

const app = express();
const port = 3000;
app.use(express.json());

// Confirm the database connection
pool.query('SELECT 1')
  .then(() => console.log('Database connection successful'))
  .catch((err) => console.error('Database connection error', err.stack));

// Serve the table page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Latest rows as JSON, fetched by index.html
app.get('/api/light', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM light_data ORDER BY recorded_at DESC LIMIT 10');
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Error retrieving data' });
  }
});

app.post('/data', (req, res) => {
  const data = req.body;
  console.log('Received data:', data);
})

app.listen(port, () => {
  console.log(`running on port ${port}`);
})