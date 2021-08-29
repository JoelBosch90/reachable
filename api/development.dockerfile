# Use Python 3.
FROM python:3

# Use the new working directory.
WORKDIR /api

# Copy over all package manager files. Make sure the django user has access.
COPY requirements.txt ./

# Install all dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the directory.
COPY . .

# We want to host the API at port 3000.
EXPOSE 3000

# Start the API server in development mode.
CMD ["python", "./server.py"]
