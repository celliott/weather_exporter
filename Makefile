include defaults.mk
export

.PHONY: up

validate :
	docker-compose config --quiet

build : validate
	docker-compose build

push :
	docker-compose push

up :
	docker-compose up -d

down :
	docker-compose down

tail :
	docker logs -f $(CONTAINER)

shell :
	docker exec -ti $(CONTAINER) /bin/bash

reset : down up tail
