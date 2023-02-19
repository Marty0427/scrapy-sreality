FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install -r requirements.txt

# Copy the output.html file to the app directory
COPY output.html /app/

# Set the command to run when the container starts
CMD ["python", "app.py"]
