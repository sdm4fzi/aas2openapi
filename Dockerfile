ARG APP_VERSION=0.1.5

FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the poetry files into the container
COPY ba-syx-aas-repository-client/ /app/ba-syx-aas-repository-client
COPY ba-syx-submodel-repository-client/ /app/ba-syx-submodel-repository-client
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

CMD ["python", "docker_app.py"]