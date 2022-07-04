import pytest

from xontrib_ptk_shell.environ import (
    is_completion_mode,
    is_completions_display_value,
    to_completion_mode,
    to_completions_display_value,
)


@pytest.mark.parametrize(
    "val, exp",
    [
        ("default", True),
        ("menu-complete", True),
        ("def", False),
        ("xonsh", False),
        ("men", False),
    ],
)
def test_is_completion_mode(val, exp):
    assert is_completion_mode(val) is exp


@pytest.mark.parametrize(
    "val, exp",
    [
        ("", "default"),
        (None, "default"),
        ("default", "default"),
        ("DEfaULT", "default"),
        ("m", "menu-complete"),
        ("mEnu_COMPlete", "menu-complete"),
        ("menu-complete", "menu-complete"),
    ],
)
def test_to_completion_mode(val, exp):
    assert to_completion_mode(val) == exp


@pytest.mark.parametrize(
    "val",
    [
        "de",
        "defa_ult",
        "men_",
        "menu_",
    ],
)
def test_to_completion_mode_fail(val):
    with pytest.warns(RuntimeWarning):
        obs = to_completion_mode(val)
        assert obs == "default"


@pytest.mark.parametrize(
    "val, exp",
    [
        ("none", True),
        ("single", True),
        ("multi", True),
        ("", False),
        (None, False),
        ("argle", False),
    ],
)
def test_is_completions_display_value(val, exp):
    assert is_completions_display_value(val) == exp


@pytest.mark.parametrize(
    "val, exp",
    [
        ("none", "none"),
        (False, "none"),
        ("false", "none"),
        ("single", "single"),
        ("readline", "readline"),  # todo: check this
        ("multi", "multi"),
        (True, "multi"),
        ("TRUE", "multi"),
    ],
)
def test_to_completions_display_value(val, exp):
    assert to_completions_display_value(val) == exp


@pytest.mark.parametrize("val", [1, "", "argle"])
def test_to_completions_display_value_fail(val):
    with pytest.warns(RuntimeWarning):
        obs = to_completions_display_value(val)
        assert obs == "multi"
