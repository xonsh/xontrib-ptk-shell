import pytest


@pytest.fixture
def load_with_whole_word(xsh, load_xontrib_module):
    xsh.env["XONSH_WHOLE_WORD_SHORTCUTS"] = True
    load_xontrib_module("xontrib_ptk_shell.main")


def test_loading(load_with_whole_word, xsh, create_shell):
    inp, out, shell = create_shell(xsh)
    assert shell.key_bindings.get_bindings_for_keys(("c-delete",))
