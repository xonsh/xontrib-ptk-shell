import pytest


@pytest.fixture
def ptk_shell(xonsh_execer):
    from prompt_toolkit.input import create_pipe_input
    from prompt_toolkit.output import DummyOutput

    from xontrib_ptk_shell.shell import PromptToolkitShell

    out = DummyOutput()
    with create_pipe_input() as inp:
        shell = PromptToolkitShell(
            execer=xonsh_execer, ctx={}, ptk_args={"input": inp, "output": out}
        )
        yield inp, out, shell
