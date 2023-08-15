"""Tests for the instance scheduler class."""

from package.scheduler.main import strtobool

def test_strtobool():
    assert strtobool("yes") == True
    assert strtobool("true") == True
    assert strtobool("t") == True
    assert strtobool("1") == True
    assert strtobool("no") == False
    assert strtobool("false") == False
    assert strtobool("f") == False
    assert strtobool("0") == False
    assert strtobool("foo") == False
    assert strtobool("bar") == False
    try:
        assert strtobool(1) == True
    except AttributeError:
        pass
    try:
        assert strtobool(1) == False
    except AttributeError:
        pass
    try:
        assert strtobool(0) == True
    except AttributeError:
        pass
    try:
        assert strtobool(0) == False
    except AttributeError:
        pass
