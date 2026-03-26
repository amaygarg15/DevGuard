FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3

COPY . /app
WORKDIR /app

EXPOSE 22
EXPOSE 8080

ENV API_KEY=DUMMY_KEY_FOR_TESTS_ONLY

CMD ["python3", "app.py"]
