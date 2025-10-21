.DEFAULT_GOAL ::= build

# Корневая папка проекта.
PROJECT_DIR ::= $(realpath $(dir $(realpath $(lastword $(MAKEFILE_LIST)))))

IMAGE_NAME ::= $(notdir $(PROJECT_DIR))

docker-run-tests = docker run --rm --tty \
	--user $(shell id -u) \
	--volume $(PROJECT_DIR)/tests:/tests \
	--volume $(PROJECT_DIR)/project-template/src/pages/conf.py:/tests/conf.py \
	--workdir /tests \
	$(IMAGE_NAME) \
	$(1)


.PHONY: build ## Выполняет сборку.
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: clean ## Очищает все результаты сборки.
clean:
	rm -rf tests/output
	docker rmi $(IMAGE_NAME)

.PHONY: tests ## Запускает все тесты собранного образа.
tests: html-tests pdf-tests

.PHONY: html-tests ## Запускает тесты сборки в HTML.
html-tests: build
	$(call docker-run-tests,sphinx-build -M html /tests /tests/output/html)
	xdg-open tests/output/html/html/index.html

.PHONY: pdf-tests ## Запускает все тесты сборки в PDF.
pdf-tests: build
	$(call docker-run-tests,sphinx-build -M latexpdf /tests /tests/output/pdf)
	xdg-open tests/output/pdf/latex/document.pdf
