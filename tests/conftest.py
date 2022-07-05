import pytest


@pytest.fixture
def xsh(xonsh_session, env, monkeypatch):
    # here we need XSH.exit and not mocking any
    monkeypatch.setattr(xonsh_session, "env", env)
    return xonsh_session


@pytest.fixture
def ptk_xontrib(xsh):
    from xonsh.xontribs import xontribs_load, xontribs_unload

    mod = "xontrib_ptk_shell.main"
    _, stderr, res = xontribs_load([mod], full_module=True)
    if stderr or res:
        raise Exception(f"Failed to load xontrib: {stderr} - {res}")
    yield
    xontribs_unload([mod], full_module=True)


@pytest.fixture
def ptk_shell(ptk_xontrib, xsh):
    from prompt_toolkit.input import create_pipe_input
    from prompt_toolkit.output import DummyOutput

    from xontrib_ptk_shell.shell import PromptToolkitShell

    out = DummyOutput()
    with create_pipe_input() as inp:
        shell = PromptToolkitShell(
            execer=xsh.execer, ctx={}, ptk_args={"input": inp, "output": out}
        )
        yield inp, out, shell
