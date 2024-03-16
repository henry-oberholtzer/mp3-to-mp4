import pytest
from pathlib import Path
import tempfile
import typer
import configparser

from mp3_to_mp4 import config

@pytest.fixture()
def temp_dir():
  with tempfile.TemporaryDirectory() as tempdir:
    return Path(tempdir)
  
@pytest.fixture()
def temp_cfg(temp_dir) -> config.Config:
    tmp_cfg_file = temp_dir / "config.ini"
    return config.Config(config_dir_path=temp_dir, config_file_path=tmp_cfg_file)

class TestConfig:
  def test_init_defaults(self, temp_cfg):
    assert temp_cfg.bg_color == temp_cfg.BG_COLOR
    assert temp_cfg.width == temp_cfg.WIDTH
    assert temp_cfg.height == temp_cfg.HEIGHT
    assert temp_cfg.output_fps == temp_cfg.FRAMERATE
    assert temp_cfg.image_padding == temp_cfg.IMAGE_PADDING
    assert temp_cfg.sort_filename == temp_cfg.SORT_FILENAME
  def test_update_bg_color(self, temp_cfg):
    color = "#121212"
    parser = configparser.ConfigParser()
    temp_cfg.update(bg_color=color)
    parser.read(temp_cfg.config_file_path)
    assert parser["General"]["bg_color"] == color
