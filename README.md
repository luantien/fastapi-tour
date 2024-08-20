# fastapi-tour
A fast tour to learn how to use FastAPI with SQLAlchemy and PostGreSQL

# Sample Setup 
- Create a virtual environment using `virtualenv` module in python.
```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
source venv/bin/activate

# Install depdendency packages
pip install -r requirements.txt
```
- Configure `.env` file by creating a copy from `.env.sample`
- Setup a postgres docker container
```bash
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=<your-preferred-one> -d postgres:14
```
- At `app` directory, run `alembic` migration command. Please make sure your postgres DB is ready and accessible. In case you want to use `SQLite` instead, please be sure to configure the `env.py` file in `alembic` folder to support `batch execution` since `SQLite` does not support `ALTER` command, which is needed to configure the foreign key and establish the indexes.
```bash
alembic upgrade head
```
- Run `uvicorn` web server from `app` directory (`reload` mode is for development purposes)
```bash
uvicorn main:app --reload
```