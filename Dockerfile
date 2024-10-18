FROM python:3.12

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

RUN touch README.md
RUN pip install --no-cache-dir --upgrade poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev
RUN python -m spacy download en_core_web_md

COPY run.py /app/run.py
COPY models /app/models
COPY dexbooruml /app/dexbooruml

ENV PORT=8000
EXPOSE 8000

CMD ["python", "run.py"]