FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY rest_introduction_app /app/rest_introduction_app

COPY shell_scripts /app/shell_scripts
RUN chmod -R +x ./shell_scripts

ENTRYPOINT ["/bin/sh", "./shell_scripts/run_all.sh"]