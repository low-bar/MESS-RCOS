# Database Utility

## `fill_db.py`

`fill_db.py` is an interactive Python utility for adding readings to and
viewing readings from the PostgreSQL database.

## Requirements

- Docker Desktop
- Docker Compose
- A root-level `.env` file containing:

  ```env
  POSTGRES_DB=mess_rcos
  POSTGRES_USER=mess_user
  POSTGRES_PASSWORD=your_local_password
  ```

The database utility uses `psycopg[binary]`, which is installed automatically
when its Docker image is built.

## Running the utility

Run this command from the repository root:

```powershell
docker compose up --build fill-db
```

This starts PostgreSQL, waits for it to become ready, builds the Python
container, and launches the interactive utility.

## Database connection

The `fill-db` service receives these settings from `.env`:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

Inside Docker, the utility connects to PostgreSQL using the Compose service
name `database`, not `localhost`.