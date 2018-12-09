.PHONY: build push clean

IMAGE_NAME := quay.io/app-sre/qontract-validator
IMAGE_TAG := $(shell git rev-parse --short=7 HEAD)

build:
	@docker build -t $(IMAGE_NAME):latest .
	@docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(IMAGE_TAG)

push:
	@docker push $(IMAGE_NAME):latest
	@docker push $(IMAGE_NAME):$(IMAGE_TAG)

clean:
	@rm -rf venv .tox .eggs reconcile.egg-info buid .pytest_cache
	@find . -name "__pycache__" -type d -print0 | xargs -0 rm -rf
	@find . -name "*.pyc" -delete
