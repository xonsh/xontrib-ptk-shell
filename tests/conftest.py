import pytest


@pytest.fixture
def ptk_xontrib(load_xontrib, xession):
    from xonsh.xontribs import xontribs_load, xontribs_unload

    mod = "xontrib_ptk_shell.main"
    yield xontribs_load([mod], full_module=True)
    xontribs_unload([mod], full_module=True)


@pytest.fixture
def ptk_shell(xonsh_execer, ptk_xontrib):
    from prompt_toolkit.input import create_pipe_input
    from prompt_toolkit.output import DummyOutput

    from xontrib_ptk_shell.shell import PromptToolkitShell

    out = DummyOutput()
    with create_pipe_input() as inp:
        shell = PromptToolkitShell(
            execer=xonsh_execer, ctx={}, ptk_args={"input": inp, "output": out}
        )
        yield inp, out, shell
