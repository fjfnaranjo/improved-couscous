DOCKER_CMD=docker run --rm -ti -v "$(shell pwd)":/hello -w /hello -e AWS_DEFAULT_REGION -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -p 8080:8080 hello

.PHONY: image
image:
	@docker build -t hello .

.PHONY: deploy
deploy:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && zappa deploy production'

.PHONY: test
test:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && pytest'

.PHONY: black
black:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && black *.py hello/*.py tests/*.py'

.PHONY: black-check
black-check:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && black --check *.py hello/*.py tests/*.py'

.PHONY: run
run:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && python -m hello.app'
