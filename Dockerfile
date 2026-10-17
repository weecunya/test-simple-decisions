FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache

COPY . .

CMD ["uvicorn", "app.src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]