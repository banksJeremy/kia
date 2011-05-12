pyv = 2.7

# Commands
# ========

.PHONY: clean build install __main

__main:
	make build

install:
	python$(pyv) setup.py build

build:
	python$(pyv) setup.py install


help:
	#   There's nothing to actually make yet, just dependencies.
	#   
	#   make test-all
	#   
	#   sudo make install-virtualenv-and-pip
	#                 - if missing, globally installs distribute, virtualenv
	#                   and pip, as required other makefile commands.
	#   
	#   make all      - locally installs and builds everything.
	#   
	#   make bin      - locally installs/initializes software used to
	#                   build and run this software, including:
	#                   
	#                   - bin/python
	#                   - bin/node
	#                   - bin/coffee
	#   
	#   make clean    - all removes build files.
	#   make purge    - removes all build files, libraries and software.

purge: clean
	# Removing Built Files and Requirements
	# =====================================
	rm -rf bin/ dist/ lib/ .Python node_modules/

dist/:
	# Making Build Directory
	# ======================
	mkdir dist

clean:
	# Removing Built Files
	# ====================	
	rm -rf dist/ *.pyc */*.pyc */*/*.pyc

all: bin lib/$(python)/site-packages/twisted \
	     lib/$(python)/site-packages/M2Crypto

bin: bin/python bin/pip bin/nodeenv bin/node bin/npm bin/coffee

# bin/
# ====

bin/coffee: bin/node-env/bin/coffee
	echo '#!/usr/bin/env bash' > bin/coffee
	echo '`dirname "$$0"`/node-env/bin/node `dirname "$$0"`/node_modules/coffee-script/bin/coffee "$$@"' >> bin/coffee
	chmod +x bin/coffee

bin/node: bin/node-env
	ln -sf node-env/bin/node bin/node

bin/npm: bin/node-env
	echo '#!/usr/bin/env bash' > bin/npm
	echo '`dirname "$$0"`/node-env/bin/node `dirname "$$0"`/node-env/bin/npm "$$@"' >> bin/npm
	chmod +x bin/npm

bin/nodeenv: bin/pip
	# Downloading nodeenv
	# ===================
	bin/pip install "nodeenv==0.3.4"

bin/pip: bin/python
	# Confirming pip installation...
	# ==============================
	bin/pip --version

bin/python:
	# Initializing virtualenv
	# =======================
	virtualenv --no-site-packages --python="$(python)" .

# lib/ and such
# =============

bin/node-env: bin/nodeenv
	# Downloading and Initializing node.js and npm
	# ============================================
	bin/nodeenv --node "0.4.7" --verbose bin/node-env

bin/node-env/bin/coffee: bin/npm
	# Downloading and Installing CoffeeScript
	# =======================================
	bin/npm install "coffee-script@1.1.0"

lib/$(python)/site-packages/M2Crypto: bin/pip
	# Downloading M2Crypto
	# ====================
	bin/pip install "M2Crypto==0.21.1"

lib/$(python)/site-packages/twisted: bin/pip
	# Downloading Twisted
	# ===================
	bin/pip install Twisted==11.0.0
