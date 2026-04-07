FROM python:3.12
WORKDIR /argusapp
COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv install
COPY . .
CMD ["Python","main.py"]
