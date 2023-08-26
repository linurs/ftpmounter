all: 
	help2man -N --no-discard-stderr ./ftpmounter.py -o ftpmounter.1
	python setup.py sdist
