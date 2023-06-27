FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN python3 -m pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["bash", "-c", "python3 app.py"]