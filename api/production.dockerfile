# Use the latest version of Python.
FROM python:3.9.7

# Create a user with default privileges as a worker.
RUN useradd --shell /bin/bash --create-home worker

# Create the working directory and give ownership to the worker.
RUN mkdir -p /client && chown -R worker:worker /client

# Use the new working directory.
WORKDIR /api

# Copy the application files to the directory.
COPY --chown=worker:worker . .

# Make sure that we are allowed to run the executable.
RUN chmod +x ./entrypoint.sh

# We want to make sure that we don't run the install commands as a root user.
USER worker

# Update PIP.
RUN python -m pip install --upgrade pip

# Install all dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# We want to host the API at port 3000.
EXPOSE 3000

# Start the API server.
CMD ["sh", "./entrypoint.sh"]
