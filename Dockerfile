
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY packages ./packages

RUN pip install --no-cache-dir --no-index --find-links=./packages -r requirements.txt

COPY . .

CMD ["python", "-u", "monitor.py"]




