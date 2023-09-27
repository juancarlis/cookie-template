# {{ cookiecutter.project_title }}
By: {{ cookiecutter.project_author_name }}
{{ cookiecutter.project_description }}



## Airflow 

**DEV**
Initialize database before executing airflow for the first time.
```shell
docker-compose run --rm airflow-webserver airflow db init
