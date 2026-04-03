FROM python:3.12-alpine

WORKDIR /app

COPY server.py /app/server.py

ENV APP_PORT=8000
EXPOSE 8000

CMD ["python", "/app/server.py"]
