FROM python:3.10-slim AS base

FROM base AS builder

# Do not create venv
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  PATH="$PATH:/runtime/bin" \
  PYTHONPATH="$PYTHONPATH:/runtime/lib/python3.10/site-packages" \
  # Versions:
  POETRY_VERSION=1.2.2


# System deps:
RUN apt-get update && apt-get install -y build-essential unzip wget python-dev
# Install poetry globally
RUN pip install "poetry==$POETRY_VERSION"


# Generate requirements and install *all* dependencies globally.
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt


FROM base AS runtime
# Copy installed python libraries
COPY --from=builder /runtime /usr/local

# Copy files needed for production
COPY ./api /app/api
COPY pyproject.toml /app/pyproject.toml

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/"
# we need to start both FastAPI and Faust worker inside one container
CMD ["python3", "api/app.py"]