
A feature rich [`prompt-toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit) based shell backend for Xonsh


## Installation

To install use pip:

```bash
xpip install xontrib-ptk-shell
```

## Usage

This xontrib will get loaded automatically for interactive sessions.

To stop this, set

```xonsh
$XONTRIBS_AUTOLOAD_DISABLED = {"ptk_shell", }
```


## Releasing your package

- Bump the version of your package.
- Create a GitHub release (The release notes are automatically generated as a draft release after each push).
- And publish with `poetry publish --build` or `twine`

## Credits

This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).


--------------------

## Xontrib Promotion (READ and REMOVE THIS SECTION)

**Add topics to the repository**. To show the xontrib repository in Github Topics please add topics `xonsh` and `xontrib` to the repository "About" setting. Also add thematic topics, for example,  `ssh` if your xontrib helps work with `ssh`.

**Easiest way to publish your xontrib to PyPi via Github Actions**. Users can install your xontrib via `pip install xontrib-myxontrib`. Easiest way to achieve it is to use Github Actions:

1. Register to https://pypi.org/ and [create API token](https://pypi.org/help/#apitoken).
2. Go to repository "Settings" - "Secrets" and your PyPI API token as `PYPI_API_TOKEN` as a "Repository Secret".
3. Click "Actions" link on your Github repository.
   1. Click on "New Workflow"
   2. Click "Configure" on "Publish Python Package" Action.
4. Commit the config without any changes.
5. Now when you create new Release the Github Actions will publish the xontrib to PyPi automatically. Release status will be in Actions sction.

**Add preview image**. Add the image to repository "Settings" - "Options" - "Social preview". It allows to show preview image in Github Topics and social networks.

## Todos

- pre-commit CI
- coverage CI
- automatic release
