-- Ejecutar en psql como usuario postgres
-- Ubuntu:  sudo -u postgres psql
-- Windows: SQL Shell (psql) o pgAdmin Query Tool

CREATE USER gestion_user WITH PASSWORD 'gestion123';
CREATE DATABASE gestion_educativa_db OWNER gestion_user;

\c gestion_educativa_db

ALTER SCHEMA public OWNER TO gestion_user;
GRANT ALL ON SCHEMA public TO gestion_user;
GRANT CREATE ON SCHEMA public TO gestion_user;

ALTER DEFAULT PRIVILEGES FOR USER gestion_user IN SCHEMA public
    GRANT ALL ON TABLES TO gestion_user;

ALTER DEFAULT PRIVILEGES FOR USER gestion_user IN SCHEMA public
    GRANT ALL ON SEQUENCES TO gestion_user;

ALTER DEFAULT PRIVILEGES FOR USER gestion_user IN SCHEMA public
    GRANT ALL ON FUNCTIONS TO gestion_user;

\q
