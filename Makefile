# weather_exporter docker-compose makefile

include .env

.PHONY: up

validate :
	docker-compose config

build : validate
	docker-compose build

push :
	docker push $(ORGANIZATION)/$(CONTAINER):$(VERSION)

up :
	docker-compose up -d

down :
	docker-compose down

tail :
	docker logs -f $(CONTAINER)

shell :
	docker exec -ti $(CONTAINER) /bin/bash

reset : down up tail