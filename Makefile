DOCKER_CMD_PREFIX=docker run --rm -ti
DOCKER_CMD_PATHS=-v "$(shell pwd)":/hello -w /hello
DOCKER_CMD_USER=-u $(shell id -u):$(shell id -g)
DOCKER_CMD_ENV=-e AWS_DEFAULT_REGION -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY
DOCKER_CMD_PORT=-p 8080:8080
DOCKER_CMD_IMAGE=hello

DOCKER_CMD_ZAPPA=$(DOCKER_CMD_PREFIX) $(DOCKER_CMD_PATHS) $(DOCKER_CMD_ENV) $(DOCKER_CMD_IMAGE)
DOCKER_CMD_DEV=$(DOCKER_CMD_PREFIX) $(DOCKER_CMD_PATHS) $(DOCKER_CMD_USER) $(DOCKER_CMD_ENV) $(DOCKER_CMD_IMAGE)
DOCKER_CMD_RUN=$(DOCKER_CMD_PREFIX) $(DOCKER_CMD_PATHS) $(DOCKER_CMD_USER) $(DOCKER_CMD_ENV) $(DOCKER_CMD_PORT) $(DOCKER_CMD_IMAGE)

.PHONY: image
image:
	@docker build -t hello .

.PHONY: deploy
deploy:
	@$(DOCKER_CMD_ZAPPA) sh -c '. /venv/bin/activate && zappa deploy production'

.PHONY: update
update:
	@$(DOCKER_CMD_ZAPPA) sh -c '. /venv/bin/activate && zappa update production'

.PHONY: undeploy
undeploy:
	@$(DOCKER_CMD_ZAPPA) sh -c '. /venv/bin/activate && zappa undeploy production'

.PHONY: test
test:
	@$(DOCKER_CMD_DEV) sh -c '. /venv/bin/activate && pytest'

.PHONY: black
black:
	@$(DOCKER_CMD_DEV) sh -c '. /venv/bin/activate && black *.py hello'

.PHONY: black-check
black-check:
	@$(DOCKER_CMD_DEV) sh -c '. /venv/bin/activate && black --check *.py hello'

.PHONY: isort
isort:
	@$(DOCKER_CMD_DEV) sh -c '. /venv/bin/activate && isort *.py hello'

.PHONY: isort-check
isort-check:
	@$(DOCKER_CMD_DEV) sh -c '. /venv/bin/activate && isort --check *.py hello'

.PHONY: run
run:
	@$(DOCKER_CMD_RUN) sh -c '. /venv/bin/activate && python -m hello.app'
