docker_build:
	cd app && docker build -t twitch_bot:latest .

docker_run:
	$(eval CONTAINER_ID := $(shell docker run -d -p 4000:8000 -e TWITCH_TOKEN -e INITIAL_CHANNELS twitch_bot:latest))
	@echo Container started: $(CONTAINER_ID)

docker_logs:
	docker logs $(CONTAINER_ID)

docker_stop:
	docker stop $(CONTAINER_ID)

mass_push:
	cd app && mass image push massdriver/twitch_bot -f lambda.Dockerfile -a ${ARTIFACT_ID} -r us-east-1

mass_publish:
	cd lambda_bundle && mass bundle lint
	cd lambda_bundle && mass bundle build
	cd lambda_bundle && mass bundle publish
