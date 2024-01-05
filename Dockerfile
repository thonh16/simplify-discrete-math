FROM python:3.7.0

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
CMD ["python", "app.py"]