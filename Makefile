docker_build:
	cd app && docker build -t twitch_bot:latest .

docker_run:
	$(eval CONTAINER_ID := $(shell docker run -d -p 8000:8000 --name TwitchBot --rm twitch_bot:latest))
	@echo Container started: $(CONTAINER_ID)

docker_logs:
	docker logs TwitchBot

docker_stop:
	docker stop TwitchBot

start_bot:
	cd app && uvicorn main:app --reload