VERSION = 1.0.1
PROJECT = readbooks

build:
	@echo ====================build====================
	python setup.py egg_info --egg-base /tmp sdist

package:
	@echo ====================package====================
	docker build -t ${PROJECT}:${VERSION} .
	# VERSION=$(VERSION) PROJECT=$(PROJECT) exec ./scripts/package
	# docker tag $(PROJECT):$(VERSION) $(REGISTRY)/$(PROJECT):$(VERSION)
