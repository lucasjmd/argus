FROM python:3.12
WORKDIR /argusapp
COPY . .
RUN pip install uv
RUN uv sync
CMD ["Python","main.py"]
