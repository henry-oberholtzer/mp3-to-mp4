import pytest
import tempfile
from pathlib import Path
from mp3_to_mp4 import config, cli
import mp3_to_mp4

@pytest.fixture()
def temp_dir():
  with tempfile.TemporaryDirectory() as tempdir:
    return Path(tempdir)

@pytest.fixture()
def temp_file():
  with tempfile.TemporaryFile() as temp_file:
    return temp_file
  
@pytest.fixture()
def temp_cfg(temp_dir) -> config.Config:
  tmp_cfg_file = temp_dir / "config.ini"
  return config.Config(config_dir_path=temp_dir, config_file_path=tmp_cfg_file)

@pytest.fixture()
def temp_user_cfg(temp_cfg, monkeypatch):
  monkeypatch.setattr(cli, "user_cfg", temp_cfg)
  return temp_cfg

@pytest.fixture
def os_error(mode: int = 511, parents: bool = False, exist_ok: bool = False):
  raise OSError


