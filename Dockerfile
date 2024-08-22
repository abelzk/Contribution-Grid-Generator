FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install -r scripts/requirements.txt

ENTRYPOINT ["bash", "scripts/entrypoint.sh"]
