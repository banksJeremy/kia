python = python2.7

.PHONY: help run-peer run-dns clean purge install-virtualenv-and-pip

help:
	# make help:
	# 
	#       If you have pip and virtualenv installed, you can run
	#   `make run-peer` or `make run-dns` and any required packages
	#   will be downloaded and installed into a virtualenv in this
	#   directory.
	#   
	#       If not, you can download and install them globally with
	#   `sudo make install-virtualenv-and-pip`.
	#   
	#   make run-peer
	#     runs a dnesque client/peer.
	#     
	#   make run-dns
	#     runs a DNS server connected to the local dnesque client.
	#  	
	#   make clean
	#     removes built files.
	#  
	#   make purge
	#     removes all dependencies and built files.

run-peer: bin/$(python) \
          lib/$(python)/site-packages/twisted \
          lib/$(python)/site-packages/M2Crypto
	# Running Peer
	# ============
	bin/$(python) src/main.py

run-dns: dist/
	# Running DNS Server
	# ==================
	coffee --compile --print > dist/dns.js
	node dist/dns.js

dist/:
	# Making Build Directory
	# ======================
	mkdir dist

clean:
	# Removing Built Files
	# ====================	
	rm -rf dist
	rm -rf src/*.pyc

lib/$(python)/site-packages/M2Crypto: bin/pip
	# Downloading M2Crypto
	# ====================
	bin/pip install "M2Crypto==0.21.1"

lib/$(python)/site-packages/twisted: bin/pip
	# Downloading Twisted
	# ===================
	bin/pip install Twisted==11.0.0

bin/coffee: bin/node-env/bin/coffee
	echo '#!/usr/bin/env bash' > bin/coffee
	echo '`dirname "$$0"`/node-env/bin/node `dirname "$$0"`/node-env/bin/coffee "$$@"' >> bin/coffee
	chmod +x bin/coffee

bin/node-env/bin/coffee: bin/npm
	# Downloading and Installing CoffeeScript
	# =======================================
	bin/npm install "coffee-script@1.0.1"

bin/node: bin/node-env
	ln -s node-env/bin/node bin/node

bin/npm: bin/node-env
	echo '#!/usr/bin/env bash' > bin/npm
	echo '`dirname "$$0"`/node-env/bin/node `dirname "$$0"`/node-env/bin/npm "$$@"' >> bin/npm
	chmod +x bin/npm

bin/node-env: bin/nodeenv
	# Downloading and Initializing node.js and npm
	# ============================================
	bin/nodeenv --node "0.4.3" bin/node-env

bin/nodeenv: bin/pip
	# Downloading nodeenv
	# ===================
	bin/pip install "nodeenv==0.3.0"

bin/pip: bin/$(python)
	# Confirming pip installation...
	# ==============================
	bin/pip --version

bin/$(python):
	# Initializing virtualenv
	# =======================
	virtualenv --no-site-packages --python="$(python)" .

purge:
	# Removing Built Files and Requirements
	# =====================================
	rm -rf `cat .gitignore`

install-virtualenv-and-pip:
	# Downloading and Installing distribute, pip and virtualenv (globally)
	# ====================================================================
	curl http://python-distribute.org/distribute_setup.py | "$(python)"
    curl https://github.com/pypa/pip/raw/master/contrib/get-pip.py | "$(python)"
	sudo pip install virtualenv
