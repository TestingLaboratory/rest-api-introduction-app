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

- 8080 - basics
- 8081 - auth token
- 8082 - Challenge Warmup
- 8083 - Reactor Challenge
- 8084 - CryptoCrypto Challenge
- 8085 - Coronavirus Genetics Challenge

If you're using **PyCharm Docker Plugin** just click on two green arrows near tag **services**.

# EC2 ubuntu
Before proceeding create and attach a security group for inbound traffic for TCP and ports 8080-8090
```
git clone https://github.com/TestingLaboratory/rest-api-introduction-app
cd rest-api-introduction-app
sudo apt-get install ca-certificates curl gnupg lsb-release
sudo mkdir -m 0755 -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo docker build . -t rest_intro
sudo docker container run -d --expose 8080-8089 -p 8080-8089:8080-8089 restintro

docker cleanup:
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker volume rm $(sudo docker volume ls -q)
```
