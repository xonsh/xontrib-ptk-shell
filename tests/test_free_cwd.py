from xonsh.pytest.tools import skip_if_on_unix


@skip_if_on_unix
def test_loading(xsh, load_xontrib_module):
    xsh.env["XONSH_FREE_CWD"] = True
    load_xontrib_module("xontrib_ptk_shell.main")
