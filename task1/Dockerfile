FROM python:3.10-slim

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8080/tcp

ENTRYPOINT /app/entrypoint.sh
