FROM python:3.12-alpine

WORKDIR /helper

COPY server.py /helper/server.py

ENV HELPER_PORT=9000
EXPOSE 9000

CMD ["python", "/helper/server.py"]
