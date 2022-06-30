from xonsh.built_ins import ShellDefinition, XonshSession


def _load_xontrib_(xsh: XonshSession, **_):
    # Some code in Using Python API:

    xsh.shells.append(
        ShellDefinition(
            aliases=("ptk", "prompt_toolkit", "prompt-toolkit"),
            cls="xontrib_ptk_shell.shell:PromptToolkitShell",
        )
    )
