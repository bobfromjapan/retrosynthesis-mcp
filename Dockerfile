FROM python:3.10

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y curl ca-certificates \
    && apt-get -y clean all
ENV PATH="/root/.cargo/bin/:$PATH"
ENV UV_SYSTEM_PYTHON=true \ 
    UV_COMPILE_BYTCODE=1 \
    UV_CACHE_DIR=/root/.cache/uv \
    UV_LINK_MODE=copy

COPY pyproject.toml ./
RUN pip install uv && \
    uv pip install -e .

COPY src/ ./src/
COPY data/ ./data/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]