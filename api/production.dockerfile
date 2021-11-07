# Use the latest version of Python.
FROM python:latest

# Update PIP.
RUN pip install --upgrade pip

# We want to make sure that we don't run the install commands as a root user.
RUN useradd --shell /bin/bash --create-home worker
USER worker

# Use the new working directory.
WORKDIR /api

# Copy over all package manager files. Make sure the worker user has access.
COPY --chown=worker:worker requirements.txt ./

# Install all dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the directory.
COPY --chown=worker:worker . .

# We want to host the API at port 3000.
EXPOSE 3000

# Start the API server.
CMD ["python", "./server.py"]
