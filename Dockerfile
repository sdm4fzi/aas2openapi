ARG APP_VERSION=0.2.1
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app
# Install dependencies using Poetry
RUN pip install aas2openapi==0.2.1

COPY . /app

EXPOSE 8000

CMD ["python", "docker_app.py"]