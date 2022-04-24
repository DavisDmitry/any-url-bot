FROM python:3.10-slim-buster as deps
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --no-dev

FROM python:3.10-slim-buster
RUN useradd appuser
USER appuser
COPY --from=deps /app/.venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY bot.py ./
CMD python bot.py
