FROM python:3.9-alpine

WORKDIR /usr/src/app

COPY requirements-deploy.txt ./
RUN pip install -r requirements-deploy.txt

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "-m", "gunicorn", "djangoCalculusApp.asgi:application", "-k", "uvicorn_worker.UvicornWorker", "--bind", "0.0.0.0:8000"]