FROM python:3.9-slim

RUN apt-get update && apt-get install -y gcc python3-dev

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /opt/
WORKDIR /opt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# # Use the official Python 3.8 image
# FROM python:3.8

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container
# COPY requirements.txt .

# # Install Python dependencies from requirements.txt
# RUN pip install --upgrade pip && \
#     pip install -r requirements.txt

# # Copy the rest of your application code into the container
# COPY . .

# # Expose the port your application will run on
# EXPOSE 8000

# # Define the entry point for your application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]