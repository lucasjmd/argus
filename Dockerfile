FROM python:3.12
WORKDIR /argus
COPY . .
RUN pip install uv
RUN uv sync
CMD ["python","src/core/adapters/ingestors.py"]
