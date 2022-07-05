import contextlib

import pytest


@pytest.fixture
def xsh(xonsh_session, env, monkeypatch):
    # here we need XSH.exit and not mocking any
    monkeypatch.setattr(xonsh_session, "env", env)
    return xonsh_session


@pytest.fixture
def load_xontrib_module():
    loaded = []
    from xonsh.xontribs import xontribs_load, xontribs_unload

    def _load(*names):
        _, stderr, res = xontribs_load(names, full_module=True)
        if stderr or res:
            raise Exception(f"Failed to load xontrib: {stderr} - {res}")

        loaded.extend(names)
        yield loaded

    if loaded:
        xontribs_unload(loaded, full_module=True)

    return _load


@pytest.fixture
def ptk_xontrib(xsh, load_xontrib_module):
    yield load_xontrib_module("xontrib_ptk_shell.main")


@pytest.fixture
def create_shell():
    with contextlib.ExitStack() as stack:

        def create(xsh):
            from prompt_toolkit.input import create_pipe_input
            from prompt_toolkit.output import DummyOutput

            from xontrib_ptk_shell.shell import PromptToolkitShell

            out = DummyOutput()
            inp = stack.enter_context(create_pipe_input())
            shell = PromptToolkitShell(
                execer=xsh.execer, ctx=xsh.ctx, ptk_args={"input": inp, "output": out}
            )
            return inp, out, shell

        yield create


@pytest.fixture
def ptk_shell(ptk_xontrib, xsh):
    return create_shell(xsh)
