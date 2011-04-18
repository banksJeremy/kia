python = python2.7

# Commands
# ========

.PHONY: help run-peer run-dns all bin clean purge install-virtualenv-and-pip

help:
	# make help:
	# 
	#   sudo make install-virtualenv-and-pip
	#                 - globally installs virtualenv and pip, which are
	#                   required for this makefile to function.
	#   
	#   make run-peer - runs a dnesque client/peer.
	#   make run-dns  - runs a DNS server connected to a client.
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
	#   
	# documentation might be available at github.com/jeremybanks/dnesque.


run-peer: bin/python \
          lib/$(python)/site-packages/twisted \
          lib/$(python)/site-packages/M2Crypto
	# Running Peer
	# ============
	bin/python src/main.py

run-dns: bin/coffee
	# Running DNS Server
	# ==================
	bin/coffee src/dns.coffee

purge: clean
	# Removing Built Files and Requirements
	# =====================================
	rm -rf bin/ dist/ lib/ .Python

install-virtualenv-and-pip:
	# Downloading and Installing distribute, pip and virtualenv (globally)
	# ====================================================================
	curl http://python-distribute.org/distribute_setup.py | "$(python)"
    curl https://github.com/pypa/pip/raw/master/contrib/get-pip.py | "$(python)"
	sudo pip install virtualenv

dist/:
	# Making Build Directory
	# ======================
	mkdir dist

clean:
	# Removing Built Files
	# ====================	
	rm -rf dist/ */*.pyc *.pyc

all: bin lib/$(python)/site-packages/twisted \
	     lib/$(python)/site-packages/M2Crypto

bin: bin/python bin/pip bin/nodeenv bin/node bin/npm bin/coffee

# bin/
# ====

bin/coffee: bin/node-env/bin/coffee
	echo '#!/usr/bin/env bash' > bin/coffee
	echo '`dirname "$$0"`/node-env/bin/node `dirname "$$0"`/node-env/bin/coffee "$$@"' >> bin/coffee
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
	bin/pip install "nodeenv==0.3.0"

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

bin/node-env/bin/coffee: bin/npm
	# Downloading and Installing CoffeeScript
	# =======================================
	bin/npm install "coffee-script@1.0.1"

lib/$(python)/site-packages/M2Crypto: bin/pip
	# Downloading M2Crypto
	# ====================
	bin/pip install "M2Crypto==0.21.1"

lib/$(python)/site-packages/twisted: bin/pip
	# Downloading Twisted
	# ===================
	bin/pip install Twisted==11.0.0

bin/node-env: bin/nodeenv
	# Downloading and Initializing node.js and npm
	# ============================================
	bin/nodeenv --node "0.4.3" bin/node-env
