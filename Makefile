docker_build:
	cd app && docker build -f local.Dockerfile -t twitch_bot:latest .

docker_run:
	docker run -d -p 4000:80 -e TWITCH_TOKEN -e INITIAL_CHANNELS twitch_bot:latest

start_virtual_env:
	python3 -m venv myenv
	source myenv/bin/activate
	pip install -r requirements.txt
	python3 twitch.py
