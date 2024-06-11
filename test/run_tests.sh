#!/bin/bash

# Ensure the script is run from the project root directory
cd "$(dirname "$0")/.." || exit

# Bring up the Docker containers
docker-compost up -d

# Wait for the containers to be fully up
sleep 10

# Run the test script
python3 tests/test_load_balancer.py

# Bring down the Docker containers
docker-compose down