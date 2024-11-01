run: start

start:
	docker compose -f ./docker/docker-compose.yml up -d --build

stop:
	docker compose -f ./docker/docker-compose.yml down

restart: stop run

api_log:
	docker logs -f --tail 100 $$(docker container ls |grep mf-ai:last | awk '{print $$1}')

pullQwen2.5:
	docker exec -it mf_ai_ollama ollama run qwen2.5:0.5b

dev_chat: init_projects
	cd ./mf-chat/ && npm run serve
	
git_reset:
	git fetch
	git reset --hard origin/master

init_projects:
	cd ./mf-chat/ && npm config set registry https://registry.npmmirror.com && npx yarn install && npx yarn install

build_chat: init_projects
	cd ./mf-chat/ && npm run build

update: git_reset
	cd ./mf-chat/ && npm run build