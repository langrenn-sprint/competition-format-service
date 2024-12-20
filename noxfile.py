"""Nox sessions."""

import sys

import nox
from nox_poetry import Session, session

package = "competition_format_service"
locations = "competition_format_service", "tests", "noxfile.py"
nox.options.envdir = ".cache"
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True
nox.options.sessions = (
    "lint",
    "mypy",
    "pytype",
    "unit_tests",
    "integration_tests",
    "contract_tests",
)


@session(python="3.12")
def clean(session: Session) -> None:
    """Clean the project."""
    session.run(
        "py3clean",
        ".",
        external=True,
    )
    session.run(
        "rm",
        "-rf",
        ".cache",
        external=True,
    )
    session.run(
        "rm",
        "-rf",
        ".pytest_cache",
        external=True,
    )
    session.run(
        "rm",
        "-rf",
        ".pytype",
        external=True,
    )
    session.run(
        "rm",
        "-rf",
        "dist",
        external=True,
    )
    session.run(
        "rm",
        "-rf",
        ".mypy_cache",
        external=True,
    )
    session.run(
        "rm",
        "-rf",
        ".coverage",
        external=True,
    )


@session(python="3.12")
def unit_tests(session: Session) -> None:
    """Run the unit test suite."""
    args = session.posargs
    session.install(".")
    session.install(
        "pytest",
        "pytest-mock",
        "pytest-aiohttp",
        "requests",
        "aioresponses",
    )
    session.run(
        "pytest",
        "-m unit",
        "-rA",
        *args,
        env={"CONFIG": "test", "JWT_SECRET": "secret"},
    )


@session(python="3.12")
def integration_tests(session: Session) -> None:
    """Run the integration test suite."""
    args = session.posargs or ["--cov"]
    session.install(".")
    session.install(
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "pytest-aiohttp",
        "requests",
        "aioresponses",
    )
    session.run(
        "pytest",
        "-m integration",
        "-rA",
        *args,
        env={
            "CONFIG": "test",
            "JWT_SECRET": "secret",
            "ADMIN_USERNAME": "admin",
            "ADMIN_PASSWORD": "password",
            "USERS_HOST_SERVER": "example.com",
            "USERS_HOST_PORT": "8081",
        },
    )


@session(python="3.12")
def contract_tests(session: Session) -> None:
    """Run the contract test suite."""
    args = session.posargs
    session.install(".")
    session.install(
        "pytest",
        "pytest-docker",
        "pytest_mock",
        "pytest-asyncio",
        "requests",
        "aioresponses",
    )
    session.run(
        "pytest",
        "-m contract",
        "-rA",
        *args,
        env={
            "CONFIG": "test",
            "ADMIN_USERNAME": "admin",
            "ADMIN_PASSWORD": "password",
            "USERS_HOST_SERVER": "localhost",
            "USERS_HOST_PORT": "8081",
            "JWT_SECRET": "secret",
            "JWT_EXP_DELTA_SECONDS": "60",
            "DB_NAME": "competition_formats_service",
            "DB_USER": "competition-format-service",
            "DB_PASSWORD": "password",
            "LOGGING_LEVEL": "DEBUG",
        },
    )


@session(python="3.12")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python="3.12")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
        "flake8-assertive",
        "flake8-eradicate",
    )
    session.run("flake8", *args)


@session(python="3.12")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", "--full-report", f"--file={requirements}")


@session(python="3.12")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or [
        "--install-types",
        "--non-interactive",
        "competition_format_service",
        "tests",
    ]
    session.install(".")
    session.install("mypy", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python="3.12")
def pytype(session: Session) -> None:
    """Run the static type checker using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@session(python="3.12")
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install(".")
    session.install("xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@session(python="3.12")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.install(".")
    session.install("sphinx", "sphinx_autodoc_typehints")
    session.run("sphinx-build", "docs", "docs/_build")


@session(python="3.12")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
