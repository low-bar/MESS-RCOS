FROM python:3.12-slim

WORKDIR /app

COPY software/database/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY software/database/fill_db.py .

CMD ["python", "fill_db.py"]
