"""This module provides Mp3-To-Mp4 configuration functionality."""

import configparser
from pathlib import Path

import typer

from mp3_to_mp4 import (
  CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_READ_ERROR, CONFIG_WRITE_ERROR, SUCCESS, __app_name__
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

def init_app(bg_color: str, output_dir: str) -> int:
  """ Initialize the application."""
  config_code = _init_config_file()
  if config_code != SUCCESS:
    return config_code
  create_config_code = _create_config(bg_color, output_dir)
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

def _create_config(bg_color: str, output_dir: str) -> int:
  config_parser = configparser.ConfigParser()
  config_parser["Video"] = {"bg_color": bg_color}
  config_parser["Output"] = {"output_dir": output_dir}
  try:
    with CONFIG_FILE_PATH.open("w") as file:
      config_parser.write(file)
      print(CONFIG_FILE_PATH)
  except OSError:
    return CONFIG_WRITE_ERROR
  return SUCCESS
  