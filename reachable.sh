#!/bin/bash
# File to quickly spin up a development container for the Reachable project.

# Make sure we can run Docker. This config file is not needed and on Windows it
# can cause some odd bugs causing Docker to fail.
rm ~/.docker/config.json

# Visit the project directory.
cd ~/Projects/reachable;

# Update to the latest version from the repository.
git pull;

# Spin up the Docker Compose network with the development settings.
docker-compose -f docker-compose.dev.yml up --build
