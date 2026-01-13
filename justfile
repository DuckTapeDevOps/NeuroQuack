# Variables
bot_name := "neuroquack"
port := "8080"

# Default target
default:
    @just --list

# Build Docker image
build:
    docker build -t {{bot_name}}:latest app/

# Run Docker container
docker-run:
    docker run -e REPLICATE_API_TOKEN -e REPLICATE_ORG -e MODEL_PHOTOMAKER -e MODEL_CLIP_INTERROGATOR -e MODEL_SDXL -e MODEL_BLIP -d -p {{port}}:{{port}} --name {{bot_name}} {{bot_name}}:latest

# Stop and remove Docker container
docker-stop:
    docker stop {{bot_name}} || true
    docker rm {{bot_name}} || true

# Rebuild and run
rebuild: docker-stop build docker-run

# Clean up Docker
clean:
    docker stop {{bot_name}} || true
    docker rm {{bot_name}} || true
    docker rmi {{bot_name}}:latest || true

# Local development setup
venv-clean:
    rm -rf app/venv

venv-setup: venv-clean
    cd app && python3 -m venv venv
    cd app && ./venv/bin/pip install -r requirements.txt

# Run locally
run: venv-setup
    cd app && ./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run locally (fast, assumes venv exists)
run-fast:
    cd app && ./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# MassDriver deployment
mass-push:
    mass push --env {{env_var('MASSDRIVER_ENV')}} --region {{env_var('AWS_DEFAULT_REGION')}}
