# установка Python
FROM python:3.12-alpine3.20
RUN apk update && apk upgrade

WORKDIR /usr/src/air_battle_server

COPY test_func.py .
COPY test_client.py .
COPY server.py .
COPY task_manager.py .
COPY client_handler.py .
COPY connection_distributor.py .

RUN ["mkdir", "database_storage"]
WORKDIR /usr/src/air_battle_server/database_storage

COPY database_storage/__init__.py .
COPY database_storage/db_config.py .
COPY database_storage/db_creator.py .
COPY database_storage/db_hub.py .
# COPY database_storage/profile_data.py .

WORKDIR /usr/src/air_battle_server

EXPOSE 9999

CMD ["python", "test_func.py"]