FROM python:3.11-slim

WORKDIR /app

COPY index.html .
COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
