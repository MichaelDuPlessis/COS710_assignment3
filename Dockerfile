FROM python:3.11-slim

COPY . /

VOLUME /runs
VOLUME /data

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
