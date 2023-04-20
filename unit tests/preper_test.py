import pytest
from transcriber import determine_type


def test_determine_type():
    assert determine_type("test.txt") == ".txt"
    assert determine_type("test.mp4") == ".mp4"

    with pytest.raises(Exception, match=f"File: file w/o type type could not be determined"):
        determine_type("file w/o type")
    with pytest.raises(Exception, match=f"File:  type could not be determined"):
        determine_type("")

def test_run_whisper():
    assert True


def test_run_pytess():
    assert True
