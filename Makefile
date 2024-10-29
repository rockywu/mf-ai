run: start

start:
	docker compose -f ./docker/docker-compose.yml up -d --build

stop:
	docker compose -f ./docker/docker-compose.yml down

restart: stop run

api_log:
	docker logs -f --tail 100 $$(docker container ls |grep mf-ai:last | awk '{print $$1}')

pullQwen2.5:
	docker exec -it $$(docker container ls |grep mf_ai_ollama | awk '{print $$1}') ollama run qwen2.5:0.5b