1. Open the yaml file, go to "services" section and find the postgres section

2. Under the volumes section, enter ports: -5432:5432. Please see below

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

3. Run in the command "docker-compose up airflow-init"

4. Run in the command "docker-compose up" (keep this terminal as it is, the terminal will run constantly as it is refreshing your system)
   Note: you can also just run "docker-compose up -d --nodeps --build postgres" if the image is already set up and you only need to change the postgre section.

5. Go to windows app "beaver" and add a PostgreSQL server

6. Set username and password both as airflow for the PostgreSQL server

7. Add a database in PostgreSQL by clicking the right button in the database section (in this case we set us erc20_database)

8. Go to airflow UI -> Admin -> Connections -> + (Add Connection)

9. Connection Id = eth_localhost (make sure your dag postgres_conn_id matches the connection id here); Connection Type = Postgres;
   Host = host.docker.internal; Schema = erc20_database (make sure the Schema name matches the database name you added on step 7);
   set both Login and Password to "airflow"; Port = 5432

10. After everything is setup, click test and see if it is success.
