FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /argus
ENV UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY . .
CMD ["uv","run","python","main.py"]
