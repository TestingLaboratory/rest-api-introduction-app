#Rest Api Introduction App - fundamentals and challenges 

In order to run application run following command in terminal:
`uvicorn rest_introduction_app.main:app --host=<HOST> --port=<PORT>`

example usage:
`uvicorn http_responses_app.main:app --host=0.0.0.0 --port=9001`

### How to run on docker:
Open project the main directory and run **docker-compose.yml**:
`docker-compose build`

Then run `docker-compose up --build --force-recreate -d` to start the application

Containers should be build with application and service should run on **localhost**  with port **8080** and following ports for different examples and challenges 

If you're using **PyCharm Docker Plugin** just click on two green arrows near tag **services**.
