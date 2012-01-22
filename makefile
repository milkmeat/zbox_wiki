all:
	python setup.py sdist
#	python setup.py bdist --format=zip,gztar
	python setup.py egg_info bdist_egg
