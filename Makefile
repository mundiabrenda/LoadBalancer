# Build the images
build:
	docker-compose build

# Run the containers
up:
	docker-compose up

# Stop the containers
down:
	docker-compose down

# Rebuild and restart the containers
restart: down build up
