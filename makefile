all:
	python setup.py bdist --format=zip,gztar

create_egg:
	python setup.py egg_info bdist_egg