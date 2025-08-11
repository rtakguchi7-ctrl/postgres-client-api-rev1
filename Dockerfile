FROM python:3.11-slim

WORKDIR /app

COPY app_1_modified.py /app/app.py

RUN pip install flask psycopg2-binary

EXPOSE 5000

CMD ["python", "app.py"]
