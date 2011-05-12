python = python2.7

.PHONY: __main build install clean distribute

__main:
	make build

build:
	$(python) setup.py build

install:
	$(python) setup.py install

clean:
	rm -rf build/ dist/ *.pyc */*.pyc */*/*.pyc

distribute:
	$(python) setup.py register sdist --formats=zip,gztar upload
