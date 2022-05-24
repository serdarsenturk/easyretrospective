Free, easy and reliable retrospective tool application.

****
### `Flask Setup`
```bash

# create virtual environment instance
$ python3 -m venv venv

# active venv
$ source venv/bin/activate

# deactivate venv
$ source venv/bin/deactivate

# install flask, gunicorn and pipenv
$ pip3 install flask gunicorn
$ pip3 install pipenv

# added to new libraries to requirements.txt was installed
$ pip3 freeze > requirements.txt

# create Procfile and Pipfile.lock
$ pipenv install -r requirements.txt

# install all libraries in requirements.txt
$ pip3 install -r requirements.txt

```
#### Start to Flask app following commands
```bash
$ flask run
```
****

### `Flask-PostgreSQL Setup`

#### For a postgresql use:

```bash

# Start postgreSQL on docker as `postgres` container name and enter your POSTGRES_PW and it name
docker run --name <container-name> -e POSTGRES_PASSWORD=<password> -p 5432:5432 -d postgres:latest

# Use this command for execute the container and use the postgres CLI
docker exec -it postgres  psql -U postgres <container-name>

# Authenticate to start using as postgres user.
psql -U postgres
psql -h localhost -p 5432 -U <Image> -W

docker exec -it <container_id/container_name> psql -U <user_name> <database_name>
docker exec -it d47056217a97 psql -U postgres conference_app

# Create table on Postgresql:
CREATE TABLE public.persons (id int PRIMARY KEY, lastName varchar(255), firstName varchar(255));

# CREATE DATABASE 
docker exec -it <container-name> psql -U <user> -c "CREATE DATABASE scoreboards ENCODING  'LATIN1' TEMPLATE template0 LC_COLLATE 'C' LC_CTYPE 'C';"

# Grant all privileges for user
docker exec -t postgres-docker psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;"

# If you are using default network when u entered `docker-compose up` command you have to use `172.17.0.1` host in DB_CONNECTION_STRING

```
****

### `Docker Deployment`

```bash

# Create an image
$ docker build --tag imageName .

# Create an image
$ docker tag <imageName>:latest <imageName>:v1.0.0 (versionize)

# Let’s remove the tag that we just created. To do this, we’ll use the rmi command. The rmi command stands for remove image.
$ docker rmi <imageName>:v1.0.0

# Start container
$ docker run <imageName>

# Execute docker container with interactive
$ docker exec -it <containerName>  psql -U <user> <databaseName>

# We did not specify a port when running the flask application in the container and the default is 5000. If we want our previous request going to port 8000 to work we can map the host’s port 8000 to the container’s port 5000:
$ docker run --publish 8000:5000 <imageName>

# Run in detechad mode
$ docker run -d -p 8000:5000 <imageName> <containerId>

# Build docker-compose.yml
$ docker-compose build

# Compose docker-compose.yml
$ docker-compose up

```
****

### `Alembic Setup:`
Alembic environment settings:
```
export DB_CONNECTION_STRING=postgresql://postgres:mysecretpassword@0.0.0.0:5432/easyretrospective
```

#### Alembic commands
```bash
Initialize flask-alembic
$ flask db init

Create new revision file by manuel
$ flask db revision -m "Message"

Autogenarate a new revision file
$ flask db migrate

Upgrade to a later version
$ flask db upgrade
```
****

### `Firebase-Admin Certificate example`

Create `cert` variable to store firebase-sdk environemnt variables to pass firebase credentials function. 
```bash
cert = {
    "type": "service_account",
    "project_id": app.config.get("PROJECT_ID"),
    "private_key_id": app.config.get("PRIVATE_KEY_ID"),
    "private_key": app.config.get("PRIVATE_KEY"),
    "client_email": app.config.get("CLIENT_EMAIL"),
    "client_id": app.config.get("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": app.config.get("CLIENT_X509_CERT_URL"),
}
```
Then you just need to pass `app.config.["FIREBASE_ADMIN_CREDENTIAL"]` `cert ` variable.
****

### `Heroku Deployment`
Download and install the Heroku CLI

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.
```bash
$ heroku login
```

Deploy your changes
```bash
$ git add .
$ git commit -am "make it better"
$ git push heroku main
```
***

### `Heroku postgresql commands`

* Use the heroku addons command to determine whether your app already has Heroku Postgres provisioned:
```bash
$ heroku addons
```

* If heroku-postgresql doesn’t appear in your app’s list of add-ons, you can provision it with the following CLI command:
```bash
$ heroku addons:create heroku-postgresql:<PLAN_NAME>
```

* To see if your database is running on legacy infrastructure, use pg:info
```bash
$ heroku pg:info
```

* To connect postgresql shell on Heroku
```bash
$ heroku pg:psql
```