# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install AWS CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    awscli && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "main.py"]
