"""Test initialization of prompt_toolkit shell"""

import sys

import pyte
import pytest
from xonsh.shell import Shell

from xontrib_ptk_shell.shell import tokenize_ansi

# verify error if ptk not installed or below min


@pytest.mark.parametrize(
    "ini_shell_type, exp_shell_type",
    [
        ("readline", "readline"),
        ("prompt_toolkit", "prompt_toolkit"),
        ("ptk", "ptk"),
        ("best", "ptk"),
    ],
)
def test_it_chooses_shell_given(ini_shell_type, exp_shell_type, ptk_xontrib):
    old_syspath = sys.path.copy()

    act_shell_type = Shell.choose_shell_type(ini_shell_type, {})

    assert len(old_syspath) == len(sys.path)

    sys.path = old_syspath

    assert act_shell_type == exp_shell_type


@pytest.mark.parametrize(
    "prompt_tokens, ansi_string_parts",
    [
        # no ansi, single token
        ([("fake style", "no ansi here")], ["no ansi here"]),
        # no ansi, multiple tokens
        ([("s1", "no"), ("s2", "ansi here")], ["no", "ansi here"]),
        # ansi only, multiple
        ([("s1", "\x1b[33mansi \x1b[1monly")], ["", "ansi ", "only"]),
        # mixed
        (
            [("s1", "no ansi"), ("s2", "mixed \x1b[33mansi")],
            ["no ansi", "mixed ", "ansi"],
        ),
    ],
)
def test_tokenize_ansi(prompt_tokens, ansi_string_parts):
    ansi_tokens = tokenize_ansi(prompt_tokens)
    for token, text in zip(ansi_tokens, ansi_string_parts):
        assert token[1] == text


@pytest.mark.parametrize(
    "line, exp",
    [
        [repr("hello"), None],
        ["2 * 3", "6"],
    ],
)
def test_ptk_prompt(line, exp, ptk_shell, capsys):
    inp, out, shell = ptk_shell
    inp.send_text(f"{line}\nexit\n")  # note: terminate with '\n'
    shell.cmdloop()
    screen = pyte.Screen(80, 24)
    stream = pyte.Stream(screen)

    out, _ = capsys.readouterr()

    # this will remove render any color codes
    stream.feed(out.strip())
    out = screen.display[0].strip()

    assert out.strip() == (exp or line)


@pytest.mark.parametrize(
    "cmd,exp_append_history",
    [
        ("", False),
        ("# a comment", False),
        ("print('yes')", True),
    ],
)
def test_ptk_default_append_history(cmd, exp_append_history, ptk_shell, monkeypatch):
    """Test that running an empty line or a comment does not append to history.
    This test is necessary because the prompt-toolkit shell uses a custom _push() method that is different from the base shell's push() method.
    """
    inp, out, shell = ptk_shell
    append_history_calls = []

    def mock_append_history(**info):
        append_history_calls.append(info)

    monkeypatch.setattr(shell, "_append_history", mock_append_history)
    shell.default(cmd)
    if exp_append_history:
        assert len(append_history_calls) == 1
    else:
        assert len(append_history_calls) == 0
