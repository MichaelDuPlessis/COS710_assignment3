FROM python:3.11

COPY . /

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
