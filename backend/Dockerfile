# Using a specific minor version of Python for better control over the Python environment
FROM python:3.10-slim-bullseye 



# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /ANIRECS
# Install poetry
RUN pip install -U pip \
    && pip install poetry

# Configure poetry:
# 1. Virtual environments cause issues in containers, so we disable their creation.
# 2. Ensure poetry installs to the system directly, ignoring the PyPI source repository.
ENV POETRY_VERSION=1.1.12 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PATH="$POETRY_HOME/bin:$PATH"

# Copy only the files necessary for installing dependencies to avoid Docker cache busting
COPY ./poetry.lock ./pyproject.toml ./

# Install project dependencies
RUN poetry install 

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application using poetry to handle the environment
CMD ["poetry", "run", "uvicorn", "anirecs.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
