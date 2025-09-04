# Use Python 3.11 for better compatibility
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set default model versions (can be overridden by environment variables)
ENV MODEL_PHOTOMAKER=jd7h/photomaker:latest
ENV MODEL_CLIP_INTERROGATOR=pharmapsychotic/clip-interrogator:8151e1c9f47e696fa316146a2e35812ccf79cfc9eba05b11c7f450155102af70
ENV MODEL_SDXL=stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc
ENV MODEL_BLIP=ducktapedevops/blip
ENV MODEL_BACKGROUND_REMOVAL=ducktapedevops/bg-rm
ENV MODEL_EMOJI=ducktapedevops/emoji

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]