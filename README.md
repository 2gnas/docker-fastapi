# docker-fastapi
Basic implementation of a containerized Python/FastAPI-powered CRUD app using a MySQL database.
Upon launch, a MySQL 5.7 container is started under the default 3306 port, which automatically imports the included initdb.sql database dump. Aside from the obvious, the database dump in question also imports 500 random entries to the table, and creates a read-only user under 'readonlyuser' for safe viewing. Local Docker volumes are mounted, and a conservative health check is ran. This may take around 30 seconds or so as is, although it can certainly be optimized with looser implementations.
Once the database is successfully started and deemed healthy, the aforementioned CRUD API is built and launched as per the included Dockerfile under the 8000 port.

# MISSING
API authentication/authorization

# SETUP
1. Set up [Docker](https://docs.docker.com/get-started/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) - 2.31.0 was used during testing;
2. Launch using `docker compose up -d` - feel free to adjust the config file before doing so.
