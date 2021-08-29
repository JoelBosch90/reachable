# Use Python 3.
FROM python:3

# Create the working directory and give ownership to the django user.
RUN mkdir -p /api && chown -R django:django /api

# Use the new working directory.
WORKDIR /api

# Copy over all package manager files. Make sure the django user has access.
COPY --chown=django:django requirements.txt ./

# Use the node user to run the install commands.
USER django

# Install all dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the directory.
COPY --chown=django:django . .

# We want to host the API at port 3000.
EXPOSE 3000

# Start the API server in development mode.
CMD ["python", "./server.py"]
