"""This module provides Mp3-To-Mp4 configuration functionality."""

import configparser
import os
from pathlib import Path

import typer

from mp3_to_mp4 import (
  ERRORS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_READ_ERROR, CONFIG_WRITE_ERROR, SUCCESS, __app_name__
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

DEFAULT_VIDEO_BG_COLOR = "#000000"
DEFAULT_VIDEO_HEIGHT = 1080
DEFAULT_VIDEO_WIDTH = 1920
DEFAULT_VIDEO_FRAMERATE = 2
DEFAULT_VIDEO_OUTPUT = Path.home() / __app_name__
DEFAULT_IMAGE_PADDING = 0
DEFAULT_SORT = True

GENERAL = "General"

def init_app(**kwargs) -> int:
  """ Initialize the application."""
  config_code = _init_config_file()
  if config_code != SUCCESS:
    return config_code
  create_config_code = _create_config(**kwargs)
  if create_config_code != SUCCESS:
    return create_config_code
  return SUCCESS
  
def _init_config_file() -> int:
  try:
    CONFIG_DIR_PATH.mkdir(exist_ok=True)
  except OSError:
    return CONFIG_DIR_ERROR
  try:
    CONFIG_FILE_PATH.touch(exist_ok=True)
  except OSError:
    return CONFIG_FILE_ERROR
  return SUCCESS

def _create_config(**kwargs) -> int:
  config_parser = configparser.ConfigParser()
  config_parser[GENERAL] = kwargs
  try:
    with CONFIG_FILE_PATH.open("w") as file:
      config_parser.write(file)
  except OSError:
    return CONFIG_WRITE_ERROR
  return SUCCESS

class RenderConfig:
  def __init__(self, config_path: Path):
    config = configparser.ConfigParser()
    config.read(config_path)
    self.bg_color = config[GENERAL]["bg_color"]
    self.output_dir = config[GENERAL]["output_dir"]
    self.width = int(config[GENERAL]["width"])
    self.height = int(config[GENERAL]["height"])
    self.image_padding = int(config[GENERAL]["image_padding"])
    self.sort_filename = bool(config[GENERAL]["sort_filename"])
    self.output_fps = int(config[GENERAL]["output_fps"])
