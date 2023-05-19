FROM python:3.11

COPY . /

VOLUME /runs

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
