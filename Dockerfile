FROM python:3.12
WORKDIR /argus
COPY . .
RUN pip install uv
RUN uv sync
CMD ["uv","run","python","-m","src.core.adapters.ingestors"]
