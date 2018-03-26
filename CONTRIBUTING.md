# Contributing to MoonTracker

## Reporting Bugs

Bugs are tracked using [GitHub issues](https://guides.github.com/features/issues/).
MoonTracker doesn't use any specific issue template, but keep the following in mind before you submit a bug.
* Ensure the bug has not already been submitted by performing a cursory search over the issue tracker.
* Be clear and descriptive in describing the bug.
* Describe the exact steps necessary to reproduce the bug.

## Feature Requests

Feature requests are tracked using [GitHub issues](https://guides.github.com/features/issues/).
MoonTracker doesn't use any specific issue template, but keep the following in mind before you submit a feature request.
* Provide a clear description of your suggested feature.
* Explain why you believe your feature is useful.
* Provide examples of the expected behavior of your feature.

## Style Guide

The style of all files in the project can be checked automatically using the [run_all_checks.sh](run_all_checks.sh) bash file.

### Python Style Guide

All Python code must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).

In addition, we also require Python code to be verified by [pyflakes](https://github.com/megies/pyflakes).

Code can be checked against both requirements automatically using [flake8](http://flake8.pycqa.org/en/latest/).

``` bash
flake8
```

### Documentation Style Guide

All Python documentation must adhere to [PEP 257](https://www.python.org/dev/peps/pep-0257/).

Documentation can be checked automatically using [pydocstyle](https://github.com/PyCQA/pydocstyle).

``` bash
pydocstyle
```

Other documentation files in the project should use [Markdown](https://daringfireball.net/projects/markdown/).
