import pytest
from pathlib import Path
import typer
import configparser
from mp3_to_mp4.config import BACKGROUND_BLUR, BACKGROUND_GROW, FONT_COLOR, IMAGE_PADDING, OUTPUT_PATH, Config, DEFAULTS, WIDTH, HEIGHT, BG_COLOR, FONT, FONT_SCALE

from mp3_to_mp4 import CONFIG_PARAM_ERROR, SUCCESS, ERRORS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_WRITE_ERROR

def os_error(mode: int = 511, parents: bool = False, exist_ok: bool = False):
  raise OSError


@pytest.fixture
def cfg(temp_cfg_file):
  return Config(temp_cfg_file)

class TestConfig:
  def test_init(self, cfg: Config):
    assert cfg.width == DEFAULTS[WIDTH]
    assert cfg.height == DEFAULTS[HEIGHT]
    assert cfg.bg_color == DEFAULTS[BG_COLOR]
    assert cfg.font == DEFAULTS[FONT]
    assert cfg.font_scale == DEFAULTS[FONT_SCALE]
    assert cfg.font_color == DEFAULTS[FONT_COLOR]
    assert cfg.image_padding == DEFAULTS[IMAGE_PADDING]
    assert cfg.background_blur == DEFAULTS[BACKGROUND_BLUR]
    assert cfg.background_grow == DEFAULTS[BACKGROUND_GROW]
    assert cfg.output_path == DEFAULTS[OUTPUT_PATH]
  def test_update(self, cfg: Config, temp_dir: Path):
    path = Path(temp_dir / "config.ini")
    cfg.create_config_file(temp_dir, path)
    assert cfg.update(path) == SUCCESS
  def test_create_config_file(self, cfg: Config, temp_dir):
    path = Path(temp_dir / "config.ini")
    assert cfg.create_config_file(temp_dir, path) == SUCCESS
  def test_remove_config_file(self, cfg: Config, temp_dir):
    path = Path(temp_dir / "config.ini")
    cfg.create_config_file(temp_dir, path)
    assert Path.exists(path) == True
    cfg.remove_config_file(path)
    assert Path.exists(path) == False
  def test_update_config(self, cfg: Config, temp_dir):
    path = Path(temp_dir / "config.ini")
    cfg.create_config_file(path.parent, path)
    cfg.bg_color = "#121212"
    cfg.update(path)
    cfg.bg_color = "#000000"
    cfg.read(path)
    assert cfg.bg_color == "#121212"
