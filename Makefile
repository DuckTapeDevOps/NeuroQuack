docker_build:
	cd app && docker build -t twitch_bot:latest .

docker_run:
	$(eval CONTAINER_ID := $(shell docker run -d -p 4000:8000 -e TWITCH_TOKEN -e INITIAL_CHANNELS twitch_bot:latest))
	@echo Container started: $(CONTAINER_ID)

docker_logs:
	docker logs $(CONTAINER_ID)

docker_stop:
	docker stop $(CONTAINER_ID)

