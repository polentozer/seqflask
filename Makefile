SRCPATH := $(CURDIR)
PROJECTNAME := $(shell basename $(CURDIR))

define HELP
Manage $(PROJECTNAME). Usage:

make run		- Run $(PROJECTNAME)
make deploy		- Install requirements and run app for the first time.
make clean		- Remove cached files and lock files.
endef
export HELP

.PHONY: run deploy clean

requirements: .requirements.txt
env: env/bin/activate

.requirements.txt: requirements.txt
	$(shell . env/bin/activate && pip install -r requirements.txxt)

all help:
	@echo "$$HELP"

.PHONY: run
run: env
	$(shell . env/bin/activate && flask run)

.PHONY: deploy
deploy:
	$(shell . ./deploy.sh)

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name 'pipefile.lock' -delete
