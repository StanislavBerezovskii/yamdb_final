# CI/CD for API YAMDB project

## Technology Stack
[![yamdb_final](https://github.com/StanislavBerezovskii/yamdb_final/workflows/yamdb_final/badge.svg)](https://github.com/StanislavBerezovskii/yamdb_final/actions/workflows/yamdb_workflow.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)
[![Practicum.Yandex](https://img.shields.io/badge/-Practicum.Yandex-464646?style=flat&logo=Practicum.Yandex&logoColor=56C0C0&color=008080)](https://practicum.yandex.ru/)


## Workflow:

* tests - Check the code for PEP8 compliance (using the flake8 package) and runs pytest. Further steps will only be executed if the push was to the master or main branch.
* build_and_push_to_docker_hub - Builds and delivers Docker images to Docker Hub
* deploy - Automatically deploys the project to the production server. Files are copied from the DockerHub repository to the server
* send_message - Sends a notification to Telegram

### Preparing to start workflow:

Create and activate the virtual environment, update pip:
```
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
```
Run autotests:
```
pytest
```
Edit the `nginx/default.conf` file and enter the IP of the virtual machine (server) in the `server_name` line.
Copy the prepared `docker-compose.yaml` and `nginx/default.conf` files from your project to the server:
Login to the repository on your local machine and upload files to the server:
```
scp ./infra/docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>:/home/<username>/nginx/default.conf
```
In the GitHub repository, add the data to `Settings - Secrets - Actions secrets`:
```
DOCKER_USERNAME - DockerHub username
DOCKER_PASSWORD - DockerHub user password
HOST - server ip address
USER - user
SSH_KEY - private ssh key (public ssh key must be on the server)
PASSPHRASE - passphrase for ssh key
DB_ENGINE - django.db.backends.postgresql
DB_HOST - db
DB_PORT - 5432
SECRET_KEY - django app secret key (try avoiding brackets if possible)
DEBUG - whether development mode is enabled (True or False)
TELEGRAM_TO - id of your telegram account (you can get it from @userinfobot, command: /start)
TELEGRAM_TOKEN - bot token (you can get a token from @BotFather, /token, bot name)
DB_NAME - postgres (default)
POSTGRES_USER - postgres (default)
POSTGRES_PASSWORD - postgres (default)
```

## Running the project on the production server:


Install Docker and Docker-compose:
```
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt install docker-compose
```
Check that Docker-Compose is installed correctly:
```
sudo  docker-compose --version
```

### After successful deployment, make sure the system is working correctly:

Collect static files:
```
sudo docker-compose exec -T web python manage.py collectstatic --no-input
```
Apply migrations:
```
sudo docker-compose exec -T web python manage.py makemigrations
sudo docker-compose exec -T web python manage.py migrate
```
Create a superuser:
```
sudo docker-compose exec web python manage.py createsuperuser
```
Unpack the data for the DB:
```
sudo docker-compose exec web python manage.py csv_to_db
```
or download the DB dump file:
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
## Open Source License:

GPL v3 (can check in gpl-3.0.md file)

## Author:

Stanislav Berezovskii

## Project URLs:

http://<server-ip>/api/v1/
http://<server-ip>/admin/
http://<server-ip>/redoc/
