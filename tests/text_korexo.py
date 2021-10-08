import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

from pathlib import Path
cwd = Path(os.path.dirname(__file__))

import korexo_profile


def text_example1():
    data = korexo_profile.read(cwd / "example1.csv")

def text_example2():
    data = korexo_profile.read(cwd / "example2.csv")
    
