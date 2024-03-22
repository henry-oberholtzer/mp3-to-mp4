import pytest
import tempfile
from pathlib import Path
from mp3_to_mp4 import config, cli

@pytest.fixture()
def temp_dir():
  with tempfile.TemporaryDirectory() as tempdir:
    return Path(tempdir)

@pytest.fixture()
def temp_mp3():
  with tempfile.TemporaryFile(suffix=".mp3") as temp_file:
    return temp_file
  
@pytest.fixture()
def temp_cfg_file(temp_dir) -> Path:
  return Path(temp_dir / "config.ini")

@pytest.fixture()
def temp_user_cfg(temp_cfg, monkeypatch):
  monkeypatch.setattr(cli, "user_cfg", temp_cfg)
  return temp_cfg
