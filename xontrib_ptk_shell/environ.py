import typing as tp
import warnings

from xonsh.environ import Env, Var, VarKeyType
from xonsh.platform import os_environ
from xonsh.tools import (
    always_false,
    dict_to_str,
    ensure_string,
    is_int,
    is_str_str_dict,
    to_int_or_none,
    to_str_str_dict,
)

CANONIC_COMPLETION_MODES = frozenset({"default", "menu-complete"})


def is_completion_mode(x):
    """Enumerated values of $COMPLETION_MODE"""
    return x in CANONIC_COMPLETION_MODES


def is_completions_display_value(x):
    """Enumerated values of ``$COMPLETIONS_DISPLAY``"""
    return x in {"none", "single", "multi"}


def to_completions_display_value(x):
    """Convert user input to value of ``$COMPLETIONS_DISPLAY``"""
    x = str(x).lower()
    if x in {"none", "false"}:
        x = "none"
    elif x in {"multi", "true"}:
        x = "multi"
    elif x in {"single", "readline"}:
        pass
    else:
        msg = f'"{x}" is not a valid value for $COMPLETIONS_DISPLAY. '
        msg += 'Using "multi".'
        warnings.warn(msg, RuntimeWarning)
        x = "multi"
    return x


def to_completion_mode(x):
    """Convert user input to value of $COMPLETION_MODE"""
    y = str(x).casefold().replace("_", "-")
    y = (
        "default"
        if y in ("", "d", "xonsh", "none", "def")
        else "menu-complete"
        if y in ("m", "menu", "menu-completion")
        else y
    )
    if y not in CANONIC_COMPLETION_MODES:
        warnings.warn(
            f"'{x}' is not valid for $COMPLETION_MODE, must be one of {CANONIC_COMPLETION_MODES}.  Using 'default'.",
            RuntimeWarning,
        )
        y = "default"
    return y


def ptk2_color_depth_setter(x):
    """Setter function for $PROMPT_TOOLKIT_COLOR_DEPTH. Also
    updates os.environ so prompt toolkit can pickup the value.
    """
    x = str(x)
    if x in {
        "DEPTH_1_BIT",
        "MONOCHROME",
        "DEPTH_4_BIT",
        "ANSI_COLORS_ONLY",
        "DEPTH_8_BIT",
        "DEFAULT",
        "DEPTH_24_BIT",
        "TRUE_COLOR",
    }:
        pass
    elif x in {"", None}:
        x = ""
    else:
        msg = f'"{x}" is not a valid value for $PROMPT_TOOLKIT_COLOR_DEPTH. '
        warnings.warn(msg, RuntimeWarning)
        x = ""
    if x == "" and "PROMPT_TOOLKIT_COLOR_DEPTH" in os_environ:
        del os_environ["PROMPT_TOOLKIT_COLOR_DEPTH"]
    else:
        os_environ["PROMPT_TOOLKIT_COLOR_DEPTH"] = x
    return x


class Xettings:
    @classmethod
    def get_settings(cls) -> tp.Iterator[tp.Tuple[VarKeyType, Var]]:
        for var_name, var in vars(cls).items():
            if not var_name.startswith("__") and var_name.isupper():
                yield var.get_key(var_name), var

    @staticmethod
    def _get_groups(
        cls, _seen: tp.Optional[tp.Set["Xettings"]] = None, *bases: "Xettings"
    ):
        if _seen is None:
            _seen = set()
        subs = cls.__subclasses__()

        for sub in subs:
            if sub not in _seen:
                _seen.add(sub)
                yield (*bases, sub), tuple(sub.get_settings())
                yield from Xettings._get_groups(sub, _seen, *bases, sub)

    @classmethod
    def get_groups(
        cls,
    ) -> tp.Iterator[
        tp.Tuple[tp.Tuple["Xettings", ...], tp.Tuple[tp.Tuple[VarKeyType, Var], ...]]
    ]:
        yield from Xettings._get_groups(cls)

    @classmethod
    def get_doc(cls):
        import inspect

        return inspect.getdoc(cls)

    @classmethod
    def get_group_title(cls) -> str:
        doc = cls.get_doc()
        if doc:
            return doc.splitlines()[0]
        return cls.__name__

    @classmethod
    def get_group_description(cls) -> str:
        doc = cls.get_doc()
        if doc:
            lines = doc.splitlines()
            if len(lines) > 1:
                return "\n".join(lines[1:])
        return ""


# topic prompt settings
class PTKSetting(Xettings):  # sub-classing -> sub-group
    """Prompt Toolkit shell
    Only usable with ``$SHELL_TYPE=prompt_toolkit.``
    """

    AUTO_SUGGEST = Var.with_default(
        True,
        "Enable automatic command suggestions based on history, like in the fish "
        "shell.\n\nPressing the right arrow key inserts the currently "
        "displayed suggestion. ",
    )
    AUTO_SUGGEST_IN_COMPLETIONS = Var.with_default(
        False,
        "Places the auto-suggest result as the first option in the completions. "
        "This enables you to tab complete the auto-suggestion.",
    )
    MOUSE_SUPPORT = Var.with_default(
        False,
        "Enable mouse support in the ``prompt_toolkit`` shell. This allows "
        "clicking for positioning the cursor or selecting a completion. In "
        "some terminals however, this disables the ability to scroll back "
        "through the history of the terminal. Only usable with "
        "``$SHELL_TYPE=prompt_toolkit``",
    )
    PROMPT_TOOLKIT_COLOR_DEPTH = Var(
        always_false,
        ptk2_color_depth_setter,
        ensure_string,
        "",
        "The color depth used by prompt toolkit 2. Possible values are: "
        "``DEPTH_1_BIT``, ``DEPTH_4_BIT``, ``DEPTH_8_BIT``, ``DEPTH_24_BIT`` "
        "colors. Default is an empty string which means that prompt toolkit decide.",
    )
    PTK_STYLE_OVERRIDES = Var(
        is_str_str_dict,
        to_str_str_dict,
        dict_to_str,
        {},
        "A dictionary containing custom prompt_toolkit style definitions. (deprecated)",
    )
    VI_MODE = Var.with_default(
        False,
        "Flag to enable ``vi_mode`` in the ``prompt_toolkit`` shell.",
    )
    XONSH_AUTOPAIR = Var.with_default(
        False,
        "Whether Xonsh will auto-insert matching parentheses, brackets, and "
        "quotes. Only available under the prompt-toolkit shell.",
    )
    XONSH_COPY_ON_DELETE = Var.with_default(
        False,
        "Whether to copy words/lines to clipboard on deletion (must be set in .xonshrc file)."
        "Only available under the prompt-toolkit shell.",
    )
    XONSH_CTRL_BKSP_DELETION = Var.with_default(
        False,
        "Delete a word on CTRL-Backspace (like ALT-Backspace). "
        r"This will only work when your terminal emulator sends ``\x7f`` on backspace and "
        r"``\x08`` on CTRL-Backspace (which is configurable on most terminal emulators). "
        r"On windows, the keys are reversed.",
    )
    XONSH_WHOLE_WORD_SHORTCUTS = Var.with_default(
        False,
        doc="Enable/Disable shortcuts to jump/delete across whole (non-whitespace) words with Ctrl+Left/Right/Delete/Backspace.",
        doc_default="False",
    )
    XONSH_FREE_CWD = Var.with_default(
        False,
        doc="Windows only, to release the lock on the current directory whenever the prompt is shown.",
        doc_default="False",
    )


class AsyncPromptSetting(PTKSetting):
    """Asynchronous Prompt
    Load $PROMPT in background without blocking read-eval loop.
    """

    ASYNC_INVALIDATE_INTERVAL = Var.with_default(
        0.05,
        "When ENABLE_ASYNC_PROMPT is True, it may call the redraw frequently. "
        "This is to group such calls into one that happens within that timeframe. "
        "The number is set in seconds.",
    )
    ASYNC_PROMPT_THREAD_WORKERS = Var(
        is_int,
        to_int_or_none,
        str,
        None,
        "Define the number of workers used by the ASYC_PROPMT's pool. "
        "By default it is the same as defined by Python's concurrent.futures.ThreadPoolExecutor class.",
    )
    ENABLE_ASYNC_PROMPT = Var.with_default(
        False,
        "When enabled the prompt is rendered using threads. "
        "$PROMPT_FIELD that take long will be updated in the background and will not affect prompt speed. ",
    )


# completer settings
class PTKCompletionSetting(Xettings):
    """Prompt Toolkit tab-completion"""

    COMPLETIONS_CONFIRM = Var.with_default(
        True,
        "While tab-completions menu is displayed, press <Enter> to confirm "
        "completion instead of running command. This only affects the "
        "prompt-toolkit shell.",
    )

    COMPLETIONS_DISPLAY = Var(
        is_completions_display_value,
        to_completions_display_value,
        str,
        "multi",
        "Configure if and how Python completions are displayed by the "
        "``prompt_toolkit`` shell.\n\nThis option does not affect Bash "
        "completions, auto-suggestions, etc.\n\nChanging it at runtime will "
        "take immediate effect, so you can quickly disable and enable "
        "completions during shell sessions.\n\n"
        "- If ``$COMPLETIONS_DISPLAY`` is ``none`` or ``false``, do not display"
        " those completions.\n"
        "- If ``$COMPLETIONS_DISPLAY`` is ``single``, display completions in a\n"
        "  single column while typing.\n"
        "- If ``$COMPLETIONS_DISPLAY`` is ``multi`` or ``true``, display completions"
        " in multiple columns while typing.\n\n"
        "- If ``$COMPLETIONS_DISPLAY`` is ``readline``, display completions\n"
        "  will emulate the behavior of readline.\n\n"
        "These option values are not case- or type-sensitive, so e.g. "
        "writing ``$COMPLETIONS_DISPLAY = None`` "
        "and ``$COMPLETIONS_DISPLAY = 'none'`` are equivalent. Only usable with "
        "``$SHELL_TYPE=prompt_toolkit``",
    )
    COMPLETIONS_MENU_ROWS = Var.with_default(
        5,
        "Number of rows to reserve for tab-completions menu if "
        "``$COMPLETIONS_DISPLAY`` is ``single`` or ``multi``. This only affects the "
        "prompt-toolkit shell.",
    )
    COMPLETION_MODE = Var(
        is_completion_mode,
        to_completion_mode,
        str,
        "default",
        "Mode of tab completion in prompt-toolkit shell (only).\n\n"
        "'default', the default, selects the common prefix of completions on first TAB,\n"
        "then cycles through all completions.\n"
        "'menu-complete' selects the first whole completion on the first TAB, \n"
        "then cycles through the remaining completions, then the common prefix.",
    )
    COMPLETION_IN_THREAD = Var.with_default(
        False,
        "When generating the completions takes time, "
        "it’s better to do this in a background thread. "
        "When this is True, background threads is used for completion.",
    )
    UPDATE_COMPLETIONS_ON_KEYPRESS = Var.with_default(
        False,
        "Completions display is evaluated and presented whenever a key is "
        "pressed. This avoids the need to press TAB, except to cycle through "
        "the possibilities. This currently only affects the prompt-toolkit shell.",
    )


def register(env: Env):
    for _, vars in Xettings.get_groups():  # type: ignore
        for key, var in vars:  # type: str, Var
            env.register(
                key,
                default=var.default,
                doc=var.doc,
                validate=var.validate,
                convert=var.convert,
                detype=var.detype,
                is_configurable=var.is_configurable,
                doc_default=var.doc_default,
                can_store_as_str=var.can_store_as_str,
            )
