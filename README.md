# FastAPI and SQLModel

[***SQLModel docs***](https://sqlmodel.tiangolo.com/tutorial/fastapi/)

[***Official github tutorials***](https://github.com/tiangolo/sqlmodel/tree/main/docs_src/tutorial)

## Install dependencies

```bash
pipenv install
```

## Run app

***Note***: **Postgresql** should be runnging. See the *Postgresql* section.

- ***Option 1***:

```bash
pipenv run uvicorn main:app --reload
```

- ***Option 2***:

```bash
pipenv shell

uvicorn main:app --reload
```

## Postgresql

- ***Option 1***: `recomended`

```bash
docker-compose up -d
```

- ***Option2***:

```bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -d postgres
```

## TODO

- [ ] Make ***async*** db 
- [ ] Make ***async*** endpoints
- [ ] Modularize all
- [ ] Change CRUD for SQLCRUD


## Docs used

### SQLModel

1. [***SQLModel Teams***](https://github.com/tiangolo/sqlmodel/blob/main/docs_src/tutorial/fastapi/teams/tutorial001.py)

### Github

- [***testdrivenio***](https://github.com/testdrivenio/fastapi-sqlmodel-alembic/blob/main/project/app/db.py)

- [***NathaliaBarreiros***](https://github.com/NathaliaBarreiros/nlp_api/tree/main/nlp_api/app)

- [***Jonra1993***](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async)

- [***HamidDoost***](https://github.com/HamidDoost/user-data-handling-api/tree/main/src/app)

- [***HamidDoost***](https://github.com/HamidDoost/user-data-handling-api/tree/main/src/app)
