FROM python:3.10-slim-buster as deps
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
WORKDIR /build
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

FROM python:3.10-slim-buster
EXPOSE 8080
RUN useradd appuser
USER appuser
COPY --from=deps /build/.venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY any_url_bot any_url_bot
CMD python -m any_url_bot
