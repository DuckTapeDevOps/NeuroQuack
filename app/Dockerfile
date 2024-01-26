# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]