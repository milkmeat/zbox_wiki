all:
	python setup.py sdist upload
	python setup.py egg_info bdist_egg upload
