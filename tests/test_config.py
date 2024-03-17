import pytest
from pathlib import Path
import typer
import configparser

from mp3_to_mp4 import config, ERRORS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_WRITE_ERROR



def os_error(mode: int = 511, parents: bool = False, exist_ok: bool = False):
  raise OSError

class TestConfig:  
  def test_init_defaults(self, temp_cfg):
    assert temp_cfg.bg_color == temp_cfg.BG_COLOR
    assert temp_cfg.width == temp_cfg.WIDTH
    assert temp_cfg.height == temp_cfg.HEIGHT
    assert temp_cfg.output_fps == temp_cfg.FRAMERATE
    assert temp_cfg.image_padding == temp_cfg.IMAGE_PADDING
    assert temp_cfg.sort_filename == temp_cfg.SORT_FILENAME
  def test_update_bg_color(self, temp_cfg: config.Config):
    color = "#121212"
    parser = configparser.ConfigParser()
    temp_cfg.update(bg_color=color)
    parser.read(temp_cfg.config_file_path)
    assert parser["General"]["bg_color"] == color
    
  def test_init_config_mkdir_error(self, temp_cfg: config.Config, monkeypatch):
    monkeypatch.setattr(Path, "mkdir", os_error)
    assert temp_cfg.update(bg_color="#121212") == CONFIG_DIR_ERROR
    
  def test_init_config_touch_error(self, temp_cfg: config.Config, monkeypatch):
    monkeypatch.setattr(Path, "touch", os_error)
    assert temp_cfg.update(bg_color="#121212") == CONFIG_FILE_ERROR
    
  def test_create_config_error(self, temp_cfg: config.Config, monkeypatch):
    monkeypatch.setattr(configparser.ConfigParser, "write", os_error)
    assert temp_cfg.update(bg_color="#121212") == CONFIG_WRITE_ERROR
  
  def test_config_default_error(self, temp_cfg: config.Config, monkeypatch, capsys):
    monkeypatch.setattr(Path, "mkdir", os_error)
    with pytest.raises(typer.Exit):
      temp_cfg.restore_defaults()
    captured = capsys.readouterr()
    assert captured.out == f'Creating the config file failed with: {ERRORS[CONFIG_DIR_ERROR]}\n'
    
  def test_restore_defaults(self, temp_cfg: config.Config):
    color = "#121212"
    parser = configparser.ConfigParser()
    temp_cfg.update(bg_color=color)
    parser.read(temp_cfg.config_file_path)
    assert parser["General"]["bg_color"] == color
    temp_cfg.restore_defaults()
    parser.read(temp_cfg.config_file_path)
    assert parser["General"]["bg_color"] == temp_cfg.BG_COLOR
