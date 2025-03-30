FROM python:latest
WORKDIR /code
COPY ./app /code/app
RUN pip install mysql-connector-python "fastapi[standard]" pydantic
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]