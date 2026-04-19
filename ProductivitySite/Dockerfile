FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir "django>=6.0.2"
COPY . /app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
