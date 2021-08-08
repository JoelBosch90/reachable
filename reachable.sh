#!/bin/bash
# File to quickly spin up a development container for the Reachable project.

# Make sure we can run Docker.
rm -rf ~/.docker/config.conf

# Visit the project directory.
cd ~/Projects/reachable;

# Update to the latest version from the repository.
git pull;

# Spin up the Docker Compose network with the development settings.
docker-compose -f docker-compose.dev.yml up --build
