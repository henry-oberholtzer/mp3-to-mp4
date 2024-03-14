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

CFG_VIDEO = "Video"
CFG_OUTPUT = "Output"

def init_app(bg_color: str, output_dir: str, width: int, height: int, image_padding: int) -> int:
  """ Initialize the application."""
  config_code = _init_config_file()
  if config_code != SUCCESS:
    return config_code
  create_config_code = _create_config(bg_color, output_dir, width, height, image_padding)
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

def _create_config(bg_color: str, output_dir: str, width: int, height: int, image_padding: int) -> int:
  config_parser = configparser.ConfigParser()
  config_parser[CFG_VIDEO] = {
    "bg_color": bg_color,
    "width": width,
    "height": height,
    "image_padding": image_padding
    }
  config_parser[CFG_OUTPUT] = {"output_dir": output_dir}
  try:
    with CONFIG_FILE_PATH.open("w") as file:
      config_parser.write(file)
  except OSError:
    return CONFIG_WRITE_ERROR
  return SUCCESS

def check_config() -> int:
  if not os.path.isfile(CONFIG_FILE_PATH):
    print("No configuration file found. Creating a configuration file based on defaults.")
    app_init_error = init_app(DEFAULT_VIDEO_BG_COLOR, DEFAULT_VIDEO_OUTPUT)
    if app_init_error:
      print(
        f'Creating the config file failed with "{ERRORS[app_init_error]}',
        style="colors(9)"
      )
      raise typer.Exit(1)
  return SUCCESS

class RenderConfig:
  def __init__(self, config_path: Path):
    config = configparser.ConfigParser()
    config.read(config_path)
    self.bg_color = config[CFG_VIDEO]["bg_color"]
    self.output_dir = config[CFG_OUTPUT]["output_dir"]
    self.width = int(config[CFG_VIDEO]["width"])
    self.height = int(config[CFG_VIDEO]["height"])
    self.image_padding = int(config[CFG_VIDEO]["image_padding"])
