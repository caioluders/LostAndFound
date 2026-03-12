import importlib.util
import os
import pytest

CHECKERS_DIR = os.path.join(os.path.dirname(__file__), "..", "checkers")


def _load_checker(name):
    """Fresh import of a checker module to reset cache_domains."""
    path = os.path.join(CHECKERS_DIR, f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def load_checker():
    return _load_checker
