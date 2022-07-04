from xonsh.built_ins import ShellDefinition, XonshSession


def register_events(events):
    events.transmogrify("on_ptk_create", "LoadEvent")
    events.doc(
        "on_ptk_create",
        """
    on_ptk_create(prompter: PromptSession, history: PromptToolkitHistory, completer: PromptToolkitCompleter, bindings: KeyBindings) ->

    Fired after prompt toolkit has been initialized
    """,
    )


def _load_xontrib_(xsh: XonshSession, **_):
    # Some code in Using Python API:

    xsh.shells.append(
        ShellDefinition(
            aliases=("ptk", "prompt_toolkit", "prompt-toolkit"),
            cls="xontrib_ptk_shell.shell:PromptToolkitShell",
            featureful=True,
        )
    )

    register_events(xsh.builtins.events)

    from . import environ

    for _, vars in environ.Xettings.get_groups():  # type: ignore
        for key, var in vars:
            xsh.env[key] = var
