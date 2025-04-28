FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install grpcio grpcio-tools

EXPOSE 50051

CMD ["python", "server.py"]