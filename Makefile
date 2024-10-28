run: start

start:
	docker compose -f ./docker/docker-compose.yml up -d --build

stop:
	docker compose -f ./docker/docker-compose.yml down

restart: stop run

api_log:
	docker logs -f --tail 100 $$(docker container ls |grep mf-ai:last | awk '{print $$1}')