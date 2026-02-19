# this specifies the Dockerfile base image
FROM python:3.11-slim

# setting a working directory
WORKDIR /app

# this will copy the relavant files into the container from the host machine
COPY . .

# installing necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for flask UI and backend server 
EXPOSE 80 82

# Create the database before starting
# RUN python create_db.py

# Default command (for dev)
CMD ["python", "frontend_travel.py"]



# To build the Docker image, run:
# docker-compose build

# To run the Docker container, use:
# docker-compose up

# To stop the Docker container without removing it, use:
# docker-compose stop

# To stop and remove the container, use:
# docker-compose down

# To stop and remove the container and its volumes, use:
# docker-compose down -v

