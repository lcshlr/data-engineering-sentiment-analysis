# Data Engineering Project - Sentiment Analysis
### Team 4 : Alexis NORINDR - Bastien BERNARD - Lucas HILAIRE

## Prerequisite

- Docker installed
- Change **API_URL** value in *public/config.js* with your server IP

## Run project

Run the following command :
```
docker-compose up
```

For testing, after starting the API, run :
```
pip3 install -r api/tests/requirements.txt
pytest
```


## Devops approach

This project can be used in a devops workflow thank's to the "devops" directory.

In this dir you vill find 4 files:

- Destroy and Deploy pipelines files that can be used by a jenkins server to monitor the deployment.
- A terraform file to create the server on aws quite simply 
- A ansible playbook to launch the docker app 
