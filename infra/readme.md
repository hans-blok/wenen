# Infra — entoli-para (PostgreSQL)

## Starting

```bash
cd infra
docker compose up -d
```

## Python driver required

For DB registration by the Python runners, `psycopg2` must be available locally.
Preferably use in this repo:

```bash
pip install psycopg2-binary
```

Without this package, runners such as `ecosysteem-coordinator` will skip DB registration.

## Starting pgAdmin

Start only PostgreSQL and pgAdmin:

```bash
cd infra
docker compose up -d db pgadmin
```

Then open pgAdmin in the browser at `http://localhost:5050`.

Log in with:

| Field | Value |
|---|---|
| E-mail | `johannes.blok@gmail.com` |
| Password | `welkom01` |

Then create a server registration in pgAdmin with these values:

| Field | Value |
|---|---|
| Name | `entoli-para` |
| Host name/address | `db` |
| Port | `5432` |
| Maintenance database | `entoli-para-db` |
| Username | `postgres_admin` |
| Password | `welkom01` |

> Within pgAdmin use `db` as host, not `localhost`, because pgAdmin runs in a separate container within the same Docker Compose network layer.

## Verbinding maken met de database

Open een interactieve `psql`-sessie in de draaiende container:

```bash
docker exec -it entoli-para psql -U postgres_admin -d entoli-para-db
```

> **Let op:** `psql` gebruikt standaard de username als databasenaam als `-d` weggelaten wordt. Geef altijd expliciet `-d <database>` mee.

| Onderdeel | Waarde | Toelichting |
|---|---|---|
| `exec -it` | interactief | koppelt terminal aan de container |
| `entoli-para` | container naam | zie `container_name` in `docker-compose.yml` |
| `psql` | PostgreSQL CLI | standaard query-tool |
| `-U postgres_admin` | database user | zie `POSTGRES_USER` in `.env` |
| `-d entoli-para-db` | database naam | zie `POSTGRES_DB` in `.env` |

## Connectiestring

```
postgresql://postgres_admin:welkom01@localhost:5432/entoli-para-db
```

Gebruik deze string voor tools zoals DBeaver, pgAdmin (extern), of een `.env` bestand in applicaties.

## Stoppen

```bash
docker compose down
```

Data blijft bewaard in het named volume `pgdata`.


## inhoud van .env
POSTGRES_USER=postgres_admin  
POSTGRES_PASSWORD=welkom01
POSTGRES_DB=entoli-para-db
