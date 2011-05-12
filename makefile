pyv = 2.7

.PHONY: __main build install clean distribute

__main:
	make build

build:
	python$(pyv) setup.py build

install:
	python$(pyv) setup.py install

clean:
	rm -rf *.pyc */*.pyc */*/*.pyc include/ build/

distribute:
	python$(pyv) setup.py register sdist --formats=zip,gztar upload
