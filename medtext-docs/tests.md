# Testing

Before contributing to medtext, make sure your patch passes our test suite
and your code style passes our code linting suite.

medtext uses [pytest](https://docs.pytest.org) to execute testing.
Before testing, make sure you have pytest installed:

```shell
$ pip install pytest pytest-cov
```

To run the full test against your changes, simply run pytest. pytest
should return without any errors. You can run pytest against all of our
environments by running:

```shell
$ pip install -e .
$ pytest --cov-report html --cov=.
```

## Continuous Integration

The medtext test suite is exercised by GitHub Actions on every push to our repo
at GitHub. You can check out the current build status:
<https://github.com/bionlplab/medtext/actions>
