FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY . /app

RUN pip install --no-cache-dir --no-build-isolation .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
