import argparse
import dataclasses
import pathlib
import subprocess
import sys
import typing
import webbrowser


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(run=lambda arguments: _help(parser))
    subparsers = parser.add_subparsers()

    for key, subcommand in _subcommands().items():
        subparser = subparsers.add_parser(key)
        subparser.set_defaults(run=subcommand.run)
        subcommand.configure_subparser(subparser)

    arguments = parser.parse_args()
    arguments.run(arguments)


def _help(parser):
    sys.exit(parser.format_help())


@dataclasses.dataclass
class _Subcommand:
    configure_subparser: typing.Callable[[argparse.ArgumentParser], None]
    run: typing.Callable[[typing.Any], None]


def _subcommands():
    def subcommand_without_arguments(run):
        return _Subcommand(
            configure_subparser=lambda subparser: None,
            run=lambda arguments: run(),
        )

    def configure_generate(subparser):
        subparser.add_argument("--open", action="store_true")
        subparser.add_argument("jupytext_path", type=pathlib.Path)

    return {
        "check": subcommand_without_arguments(_check),
        "generate": _Subcommand(
            configure_subparser=configure_generate,
            run=lambda arguments: _generate(arguments.jupytext_path, arguments.open),
        ),
        "interact": subcommand_without_arguments(_interact),
        "lint": subcommand_without_arguments(_lint),
        "test": subcommand_without_arguments(_test),
        "test_in_isolation": subcommand_without_arguments(_test_in_isolation),
        "test_without_check": subcommand_without_arguments(_test_without_check),
    }


def _check():
    working_folder = pathlib.Path.cwd()
    subprocess.run(
        [
            "docker",
            "run",
            "--entrypoint",
            "sh",
            "--rm",
            "--volume",
            f"{working_folder}:/workdir",
            "evolutics/travel-kit:0.6.0",
            "-c",
            "git ls-files -z | xargs -0 travel-kit check --skip Pylint --",
        ],
        check=True,
    )


def _generate(jupytext_path, open_):
    subprocess.run(
        [
            "jupytext",
            "--execute",
            "--from",
            "py:nomarker",
            "--set-kernel",
            "-",
            "--to",
            "notebook",
            jupytext_path,
        ],
        check=True,
    )
    jupyter_path = jupytext_path.with_suffix(".ipynb")
    subprocess.run(
        ["jupyter", "nbconvert", "--no-input", "--to", "html", jupyter_path], check=True
    )

    if open_:
        webbrowser.open(str(jupyter_path.with_suffix(".html")))


def _interact():
    subprocess.run(
        ["jupyter", "notebook", "--notebook-dir", _notebooks_folder()], check=True
    )


def _notebooks_folder():
    return pathlib.Path("src") / "notebooks"


def _lint():
    notebooks_init = _notebooks_folder() / "__init__.py"
    if not notebooks_init.exists():
        sys.exit(f"File must exist to lint notebooks: {notebooks_init}")

    subprocess.run(["pylint", "src", "tests"], check=True)


def _test():
    _check()
    _test_without_check()


def _test_without_check():
    _lint()
    subprocess.run(["pytest"], check=True)


def _test_in_isolation():
    _check()
    image = _build_docker_image("test_without_check", ["."])
    subprocess.run(
        ["docker", "run", "--rm", image, "journal", "test_without_check"],
        check=True,
    )


def _build_docker_image(tag, arguments):
    project = _project_name()
    image = f"{project}:{tag}"
    subprocess.run(["docker", "build", "--tag", image] + arguments, check=True)
    return image


def _project_name():
    raw_path = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=True,
        text=True,
    ).stdout.rstrip()
    return pathlib.Path(raw_path).name
