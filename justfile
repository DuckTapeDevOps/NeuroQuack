bot_name  := "ducktronaut"
port	  := "8080"
aws_region := env_var('AWS_DEFAULT_REGION')
# Define the default BOT variable

#PYTHON

bashrc:
	source ~/.bashrc
	start_stream

run:
	cd app && uvicorn main:app --reload

start: docker-build docker-run docker-follow

stop: docker-stop

#DOCKER
# Target to build Docker image
docker-build:
    cd app && docker build -t {{bot_name}}:latest .

# Target to run Docker container
docker-run:
    docker run -e REPLICATE_API_TOKEN -d -p {{port}}:{{port}} --name {{bot_name}} {{bot_name}}:latest 

docker-run-pull IMAGE:
	docker run -e REPLICATE_API_TOKEN -d -p {{port}}:{{port}} --name {{bot_name}} {{IMAGE}}

# Command to run both the above commands
docker-rm F:
    docker rm {{F}} {{bot_name}}
    docker rmi {{F}} {{bot_name}}:latest

# Command to remove a Docker container
docker-rm-container:
    docker rm {{bot_name}}

# Command to remove a Docker image
docker-rm-image:
    docker rmi {{bot_name}}:latest

docker-logs:
	docker logs {{bot_name}}

docker-follow:
	docker logs -f {{bot_name}}

docker-stop:
	docker stop {{bot_name}}

#MASSDRIVER
mass-push:
	cd app && mass image push massdriver/{{bot_name}} -a {{env_var('ARTIFACT_ID')}} -r {{aws_region}}

mass-publish:
	cd tofu/massdriver && mass budle publish

find-process PORT:
	ss -lptn 'sport = :{{PORT}}'
	echo "kill -9 <PID>"

rebuild: docker-stop docker-rm-container docker-build docker-run docker-follow
