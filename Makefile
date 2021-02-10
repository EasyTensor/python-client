
build-package:
	rm -rf dist && python3 -m build

publish:
	python3.9 -m twine upload dist/*

test-publish:
	python3.9 -m twine upload --repository testpypi dist/*
