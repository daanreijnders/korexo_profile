import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

from datetime import date
from pathlib import Path
cwd = Path(os.path.dirname(__file__))

import korexo_profile


def test_example1():
    data = korexo_profile.read(cwd / "example1.csv")

def test_example2():
    data = korexo_profile.read(cwd / "example2.csv")
    
def test_example2_utf8():
    data = korexo_profile.read(cwd / "example2_utf8.csv", encoding="utf-8")
    
def test_example2_utf8_encoding_fail_check():
    with pytest.raises(UnicodeDecodeError):
        data = korexo_profile.read(cwd / "example2_utf8.csv")

def test_datefmt_auto():
    data = korexo_profile.read(cwd / "example1.csv", datefmt="auto")
    datecol = data["datasets"][0]
    assert datecol["median"] == date(2019, 11, 12)

def test_datefmt_specified():
    data = korexo_profile.read(cwd / "example1.csv", datefmt="%d/%m/%Y")
    datecol = data["datasets"][0]
    assert datecol["median"] == date(2019, 12, 11)
    
def test_datefmt_specified_2():
    data = korexo_profile.read(cwd / "example1.csv", datefmt="%m/%d/%Y")
    datecol = data["datasets"][0]
    assert datecol["median"] == date(2019, 11, 12)

    