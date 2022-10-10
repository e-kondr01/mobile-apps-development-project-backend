.PHONY: up
up:
	docker compose -f production-docker-compose.yml up

.PHONY: run
run: up

.PHONY: local
local:
	docker compose -f local-docker-compose.yml up -d
	python app/manage.py migrate
	python app/manage.py runserver

.DEFAULT_GOAL := up
