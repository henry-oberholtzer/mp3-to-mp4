"""This module provides the mp3-to-mp4 configuration functionality."""
import configparser
import os
import re
from pathlib import Path

import typer

from mp3_to_mp4 import (
  ERRORS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_PARAM_ERROR, CONFIG_WRITE_ERROR, SUCCESS, __app_name__
)

class Config:
  """ Handles creating, modifying and reading the config.ini file."""
  BG_COLOR = "#000000"
  WIDTH = 1920
  HEIGHT = 1080
  FRAMERATE = 2
  OUTPUT_DIR = Path.home() / __app_name__
  IMAGE_PADDING = 0
  SORT_FILENAME = True
  GENERAL = "General"
  def __init__(self, config_dir_path: Path, config_file_path: Path):
    if not os.path.isfile(config_file_path):
      self.config_dir_path = config_dir_path
      self.config_file_path = config_file_path
      self.__config_default()
      self.__init__(config_dir_path, config_file_path=config_file_path)
    else:
      parser = configparser.ConfigParser()
      parser.read(config_file_path)
      self.config_dir_path = config_dir_path
      self.config_file_path = config_file_path
      self.bg_color = parser[self.GENERAL]["bg_color"]
      self.output_dir = Path(parser[self.GENERAL]["output_dir"])
      self.width = int(parser[self.GENERAL]["width"])
      self.height = int(parser[self.GENERAL]["height"])
      self.image_padding = int(parser[self.GENERAL]["image_padding"])
      self.sort_filename = bool(parser[self.GENERAL]["sort_filename"])
      self.output_fps = int(parser[self.GENERAL]["output_fps"])
  
  def restore_defaults(self):
    """ Restores default configuration settings. """
    return self.__config_default()

  def update(self, **kwargs) -> int:
    """ Updates the application configuration based on arguments. """
    config_code = self.__init_config_file()
    if config_code != SUCCESS:
      return config_code
    create_config_code = self.__create_config(**kwargs)
    if create_config_code != SUCCESS:
      return create_config_code
    return SUCCESS
  
  def __config_default(self):
    app_init_error = self.update(
      bg_color=self.BG_COLOR,
      output_dir=self.OUTPUT_DIR,
      width=self.WIDTH,
      height=self.HEIGHT,
      image_padding=self.IMAGE_PADDING,
      sort_filename=self.SORT_FILENAME,
      output_fps=self.FRAMERATE)
    if app_init_error:
      print(f'Creating the config file failed with: {ERRORS[app_init_error]}')
      raise typer.Exit(1)
    
  def __init_config_file(self) -> int:
    try:
      self.config_dir_path.mkdir(exist_ok=True)
    except OSError:
      return CONFIG_DIR_ERROR
    try:
      self.config_file_path.touch(exist_ok=True)
    except OSError:
      return CONFIG_FILE_ERROR
    return SUCCESS

  def __create_config(self, **kwargs) -> int:
    config_parser = configparser.ConfigParser()
    config_parser[self.GENERAL] = kwargs
    try:
      with self.config_file_path.open("w") as file:
        config_parser.write(file)
    except OSError:
      return CONFIG_WRITE_ERROR
    return SUCCESS
  
  def check_params(self, bg_color: str, width: int, height: int):
    checks = [
    self.__check_color(bg_color),
    self.__check_dimension(width),
    self.__check_dimension(height),
    ]
    if all([True if check == SUCCESS else False for check in checks]):
      return SUCCESS
    return CONFIG_PARAM_ERROR

  def __check_color(self, color: str):
    hex_regex = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    if hex_regex.fullmatch(color) == None:
      return CONFIG_PARAM_ERROR
    return SUCCESS

  def __check_dimension(self, px: int):
    if 0 < px < 3841:
      return SUCCESS
    return CONFIG_PARAM_ERROR
