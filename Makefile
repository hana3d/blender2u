.DEFAULT_GOAL := help
.PHONY: update

###################################################################################################
## SCRIPTS
###################################################################################################

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([\w-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		line = '{: <20} {}'.format(target, help)
		line = re.sub(r'^({})'.format(target), '\033[96m\\1\033[m', line)
		print(line)
endef

###################################################################################################
## VARIABLES
###################################################################################################

export PYTHON=python
export PRINT_HELP_PYSCRIPT
export BLENDER_VERSION=2.93
SHELL=/bin/bash -o pipefail
BLENDER_SCRIPTS_PATH ?= $(shell dirname $(shell readlink -f $(shell which blender)))/$(BLENDER_VERSION)/scripts/
STAGE ?= production
HANA3D_DESCRIPTION=$(shell sed -e 's/HANA3D_DESCRIPTION: \(.*\)/\1/' -e 'tx' -e 'd' -e ':x' hana3d/config/$(STAGE).yml)
HANA3D_NAME=$(shell sed -e 's/HANA3D_NAME: \(.*\)/\1/' -e 'tx' -e 'd' -e ':x' hana3d/config/$(STAGE).yml)

###################################################################################################
## GENERAL COMMANDS
###################################################################################################

help: ## show this message
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


lint: ## lint code
	isort --recursive --check .
	# new code should always get better
	xenon --max-absolute B --max-modules A --max-average A; \
	# do not let old code get worse
	xenon --max-absolute C --max-modules B --max-average A *.py --exclude addon_updater.py,addon_updater_ops.py; \
	mypy addons && exit 1 || exit 0


build: ## build addon according to stage
	# zip addon folder
	zip -rq blender2u.zip .
	# copy to ~/Downloads for easy manual install
	cp blender2u.zip ~/Downloads || true
