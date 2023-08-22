FROM python:3.7

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]