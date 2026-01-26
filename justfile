# Set shell for Windows
set shell := ["powershell.exe", "-Command"]

# Variables
bot_name := "neuroquack"
port := "8080"

# Default target
default:
    @just --list

# Build Docker image
build:
    docker build -t {{bot_name}}:latest app/

# Run Docker container (uses environment variables from your shell)
docker-run:
    docker run -e REPLICATE_API_TOKEN -e REPLICATE_ORG -e BOT_NAME -e TWITCH_ACCESS_TOKEN -e TWITCH_REFRESH_TOKEN -e TWITCH_CLIENT_ID -e MODEL_PHOTOMAKER -e MODEL_CLIP_INTERROGATOR -e MODEL_SDXL -e MODEL_BLIP -d -p {{port}}:{{port}} --name {{bot_name}} {{bot_name}}:latest

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
# Note: uv automatically handles cross-platform paths (Windows/Linux/macOS)
# Using PowerShell syntax (; instead of &&)
venv-clean:
    Set-Location app; if (Test-Path .venv) { Remove-Item -Recurse -Force .venv }; if (Test-Path venv) { Remove-Item -Recurse -Force venv }

venv-setup: venv-clean
    Set-Location app; uv sync --no-install-project

# Run locally (creates venv and installs deps if needed)
run:
    Set-Location app; uv sync --no-install-project; uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run locally (fast, assumes dependencies are synced)
run-fast: venv-setup
    Set-Location app; uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# MassDriver deployment
mass-push:
    mass push --env {{env_var('MASSDRIVER_ENV')}} --region {{env_var('AWS_DEFAULT_REGION')}}
