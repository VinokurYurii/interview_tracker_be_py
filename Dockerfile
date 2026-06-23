FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/base.txt requirements/base.txt

FROM base AS development

COPY requirements/local.txt requirements/local.txt
RUN pip install --no-cache-dir -r requirements/local.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS production

COPY requirements/production.txt requirements/production.txt
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
