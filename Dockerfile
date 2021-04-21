FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY rest_introduction_app /app/rest_introduction_app

ENTRYPOINT ["uvicorn", "rest_introduction_app.main:app", "--host", "0.0.0.0", "--port", "8080"]
