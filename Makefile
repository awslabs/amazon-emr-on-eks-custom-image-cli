test:
	# Run unit tests
	# Fail if coverage falls below 95%
    coverage run -m unittest discover
    coverage report -m --fail-under=95 --skip-empty

    coverage run --branch -m unittest discover
    coverage report -m --fail-under=95 --skip-empty