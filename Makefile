DOCKER_CMD=docker run --rm -ti -v "$(shell pwd)":/hello -w /hello -e AWS_DEFAULT_REGION -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -p 8080:8080 hello

.PHONY: image
image:
	@docker build -t hello .

.PHONY: deploy
deploy:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && zappa deploy production'

.PHONY: update
update:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && zappa update production'

.PHONY: undeploy
undeploy:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && zappa undeploy production'

.PHONY: test
test:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && pytest'

.PHONY: black
black:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && black *.py hello'

.PHONY: black-check
black-check:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && black --check *.py hello'

.PHONY: run
run:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && python -m hello.app'
