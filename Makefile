run: start

start:
	docker compose -f ./docker-compose.yml up -d --build

stop:
	docker compose -f ./docker-compose.yml down

restart: stop run