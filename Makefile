DOCKER_CMD=docker run --rm -ti -v "$(shell pwd)":/hello -w /hello -e AWS_DEFAULT_REGION -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY hello

.PHONY: image
image:
	@docker build -t hello .

.PHONY: deploy
deploy:
	@$(DOCKER_CMD) sh -c '. /venv/bin/activate && zappa deploy production'
