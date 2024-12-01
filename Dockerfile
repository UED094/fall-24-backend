FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install hatch uv

ENV PATH="/app/.venv/bin:$PATH"

RUN uv venv

RUN hatch run uv sync

EXPOSE 8000


CMD ["hatch", "run","start"]
