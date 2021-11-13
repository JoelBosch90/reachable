# Use the latest version of Python.
FROM python:latest

# Create a user with default privileges as a worker.
RUN useradd --shell /bin/bash --create-home worker

# Create the working directory and give ownership to the worker.
RUN mkdir -p /client && chown -R worker:worker /client

# We want to make sure that we don't run the install commands as a root user.
USER worker

# Use the new working directory.
WORKDIR /api

# Copy the application files to the directory.
COPY --chown=worker:worker . .

# Send python output straight through to the terminal.
ENV PYTHONUNBUFFERED=1

# Update PIP.
RUN python -m pip install --upgrade pip

# Install all dependencies.
RUN pip install --no-cache-dir -r requirements-dev.txt

# We want to host the API at port 3000.
EXPOSE 3000

# Start the API server.
CMD ["./entrypoint.sh"]
