FROM python:3.9.6-slim-buster

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.0

RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean


# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml /usr/src/app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . .

# Add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]