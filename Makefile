USERNAME=msmetko
IMAGE_NAME = test_model
TAG=latest

.PHONY: build
build:
	docker build -t ${USERNAME}/${IMAGE_NAME}:${TAG} .

.PHONY: test
test:
	docker build -t $(IMAGE_NAME)-candidate .
	IMAGE_NAME=$(IMAGE_NAME)-candidate test/run
