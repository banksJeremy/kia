python = python2.7

.PHONY: help run-peer run-dns clean virtualenv purge install-virtualenv-and-pip

help:
	# make help:
	# 
	#   make run-peer
	#     
	#     runs a dnesque client/peer.
	#     
	#   make run-dns
	#     
	#     runs a DNS server connected to the local dnesque client.
	#  	
	#   make clean
	#     
	#     removes built files.
	#  
	#   make purge
	#   
	#     removes built files and virtualenv environment.
	#   
	#   sudo make install-virtualenv-and-pip
	#   
	#     installs distribute, pip and virtualenv (globally).
	#     make will probably fail without these.

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
	# Installing M2Crypto
	# ===================
	bin/pip install "M2Crypto==0.21.1"

lib/$(python)/site-packages/twisted: bin/pip
	# Installed Twisted
	# =================
	bin/pip install Twisted==11.0.0

bin/pip: bin/$(python)
	# Verifying Availabiltity of pip
	# ==============================
	pip --version

virtualenv: bin/$(python)
bin/$(python):
	# Initializing virtualenv
	# =======================
	virtualenv --no-site-packages --python="$(python)" .

purge:
	# Removing Built Files and Requirements
	# =====================================
	rm -rf `cat .gitignore`

install-virtualenv-and-pip:
	# Downloading and Installing distribute, pip and virtualenv
	# =========================================================
	curl http://python-distribute.org/distribute_setup.py |          \
		"$(python)" &&                                               \
    curl https://github.com/pypa/pip/raw/master/contrib/get-pip.py | \
		"$(python)" &&                                               \
    sudo pip install virtualenv
