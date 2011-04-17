python = python2.7

run-peer: bin/$(python) lib/$(python)/site-packages/M2Crypto
	# Running Peer
	# ============
	bin/$(python) src/main.py

run-dns: dist
	# Running DNS Server
	# ==================
	coffee --compile --print > dist/dns.js
	node dist/dns.js

lib/$(python)/site-packages/M2Crypto: bin/pip
	bin/pip install "M2Crypto==0.21.1"

bin/pip: bin/$(python)
	# Verifying Presence of pip
	# =========================
	# 
	# (You may sudo make install-metarequirements to download if missing.)
	#
	pip --version

bin/$(python):
	# Initializing Virtualenv
	# =======================
	# 
	# (You may sudo make install-metarequirements to download if missing.)
	# 
	virtualenv --no-site-packages --python="$(python)" .

empty:
	# Removing Build and Requirements
	# ===============================
	rm -rf `cat .gitignore`

dist:
	mkdir dist

install-metarequirements:
	# Downloading and Installing distribute, pip and virtualenv
	# =========================================================
	curl http://python-distribute.org/distribute_setup.py |          \
    	"$(python)" &&                                               \
    curl https://github.com/pypa/pip/raw/master/contrib/get-pip.py | \
    	"$(python)" &&                                               \
    sudo pip install virtualenv
