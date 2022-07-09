
A feature rich [`prompt-toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit) based shell backend for Xonsh

<p align="center">
    <a href="https://codecov.io/github/xonsh/xontrib-ptk-shell?branch=main">
        <img src="https://codecov.io/gh/xonsh/xontrib-ptk-shell/branch/main/graphs/badge.svg" alt="codecov.io"/></a>
    <a href="https://github.com/xonsh/xontrib-ptk-shell/actions">
        <img src="https://github.com/xonsh/xontrib-ptk-shell/actions/workflows/test.yml/badge.svg?branch=main" alt="build status"></a>
</p>

## Installation

To install use pip:

```bash
xpip install xontrib-ptk-shell
```

## Usage

This xontrib will get loaded automatically for interactive sessions.

If installed, the `ptk-shell` will get used by default. This can also be specified explcitly by

```xonsh
$SHELL_TYPE = "ptk"

# or pass as argument
xonsh --shell-type=ptk
```

To stop this, set

```xonsh
$XONTRIBS_AUTOLOAD_DISABLED = {"ptk_shell", }
```

## Features

- [`Fish`](https://fishshell.com/) like [auto-suggesions](https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html#auto-suggestion) from history
- emacs and vi mode available
- Whole word jumping shortcuts - link doc here
- On Windows `free_cwd` - link here
- [`Fish`](https://fishshell.com/docs/current/cmds/abbr.html) like abbreviations - link here
- Asynchronous prompts

## Releasing package

- Create a GitHub release (The release notes are automatically generated as a draft release after each push).
- The package will be published to PyPI automatically by GitHub Actions.


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

- automatic release
- docs
