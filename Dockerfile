FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY client.py .

EXPOSE 8192

CMD ["/bin/bash", "-c", "python main.py"]
