bot_name  := "neuroquack"
massdriver_artifact_id := env_var('ARTIFACT_ID')
aws_region := env_var('AWS_DEFAULT_REGION')
# Define the default BOT variable

#PYTHON

python-run:
	cd app && uvicorn main:app --reload


#DOCKER
# Target to build Docker image
docker-build:
    cd app && docker build -f Dockerfile.local -t {{bot_name}}:latest .

# Target to run Docker container
docker-run:
    docker run -e REPLICATE_API_TOKEN -d -p 8000:8000 --name {{bot_name}} {{bot_name}}:latest 

docker-run-pull IMAGE:
	docker run -e REPLICATE_API_TOKEN -d -p 8000:8000 --name {{bot_name}} {{IMAGE}}

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

docker-logs-follow:
	docker logs -f {{bot_name}}

docker-stop:
	docker stop {{bot_name}}

#MASSDRIVER
mass-push:
	cd app && mass image push massdriver/{{bot_name}} -a {{massdriver_artifact_id}} -r {{aws_region}}

mass-publish:
	cd tofu/massdriver && mass budle publish
	
find-process:
	ss -lptn 'sport = :8000'
	echo "kill -9 <PID>"
