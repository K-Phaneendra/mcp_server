MCP Gateway built with FastAPI and PostgreSQL.

### create local infrastructure
A docker container with `postgresql` server and a `pgadmin` GUI will be created on using the below command
```
cd infrastructure
mkdir pgadmin
cd pgadmin
echo '{
  "Servers": {
    "1": {
      "Name": "local-postgres",
      "Group": "Servers",
      "Host": "postgres",
      "Port": 5432,
      "MaintenanceDB": "appdb",
      "Username": "appuser",
      "Password": "apppassword",
      "SSLMode": "prefer"
    }
  }
}
' > servers.json && chmod 666 servers.json
cd ..
docker compose up -d
```
Open `http://localhost:5050` on the browser to see pgadmin GUI

#### troubleshoot
If pgadmin GUI is not opening, then run `docker compose down`. Wait for couple of minutes and then run `docker compose up -d`. Wait for a couple of minutes. Now you should be able to open `http://localhost:5050` on the browser

### Credentials
#### postgresql
- POSTGRES_USER: appuser
- POSTGRES_PASSWORD: apppassword
- POSTGRES_DB: appdb

#### pgadmin
- PGADMIN_DEFAULT_EMAIL: admin@example.com
- PGADMIN_DEFAULT_PASSWORD: admin123

### load sales information in the database
Once the docker container with postgresql with pgadmin is up and running, then run the below commands to create data in the database
```
chmod +x ./scripts/load_chocolate_sales.sh
./scripts/load_chocolate_sales.sh
```
