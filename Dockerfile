FROM python:3.12-alpine AS build

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project false

COPY pyproject.toml poetry.lock* /app/

RUN echo "Versão do Poetry:" && poetry --version
RUN echo "Conteúdo do pyproject.toml:" && cat pyproject.toml

ENV YOUR_ENV=developer

RUN if [ "$YOUR_ENV" = "production" ]; then \
        poetry install --only=main --no-interaction --no-ansi --no-root; \
    else \
        poetry install --no-interaction --no-ansi --no-root; \
    fi

COPY . .

# DEBUG: Vamos ver o que foi copiado
RUN echo "=== CONTEÚDO DO DIRETÓRIO ATUAL ==="
RUN ls -la
RUN echo "=== CONTEÚDO DO DIRETÓRIO SCRIPTS ==="
RUN ls -la scripts/ || echo "Diretório scripts não existe!"
RUN echo "=== VERIFICANDO SE ENTRYPOINT.SH EXISTE ==="
RUN ls -la scripts/entrypoint.sh || echo "Arquivo entrypoint.sh não existe!"

RUN chmod +x ./scripts/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./scripts/entrypoint.sh"]