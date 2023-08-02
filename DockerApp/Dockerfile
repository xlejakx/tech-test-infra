# Use the official Python image as the base image
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the app dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY files/app/ .

# Expose the port on which your Python app listens
EXPOSE 80

# Define the command to run your Python app (replace 'app.py' with your app's main Python file)
CMD ["python", "app.py"]
