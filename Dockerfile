FROM python:3.14-slim

WORKDIR /app

COPY ./pyproject.toml ./uv.lock /app/

RUN pip install uv && uv sync

COPY . /app/

CMD ["uv", "run", "main.py"]