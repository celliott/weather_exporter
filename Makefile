include defaults.mk
export

.PHONY: up

validate :
	docker-compose config --quiet

build : validate
	docker-compose build

push : build
	docker-compose push

up :
	docker-compose up -d

down :
	docker-compose down

tail :
	docker logs -f $(SERVICE)

shell :
	docker exec -ti $(SERVICE) /bin/bash

reset : down up tail

deploy :
	helm init --client-only
	-kubectl create namespace $(SERVICE)
	helm upgrade -i $(SERVICE) helm/$(SERVICE) \
		--namespace $(SERVICE) \
		--set darkSkyAPIKey=${DARK_SKY_API_KEY} \
		--set scrapeInterval=${SCRAPE_INTERVAL} \
		--set ingress.hostname=$(SERVICE).$(DOMAIN) \
		--set ingress.enabled=false

delete :
	helm del --purge $(SERVICE)
