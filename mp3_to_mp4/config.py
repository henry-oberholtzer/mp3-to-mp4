"""This module provides the mp3-to-mp4 configuration functionality."""
import configparser
import os
import re
from pathlib import Path

from mp3_to_mp4 import ( CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_WRITE_ERROR, SUCCESS, __app_name__
)

(
  WIDTH,
  HEIGHT,
  BG_COLOR,
  ENABLE_BG_IMAGE,
  FONT,
  USE_FILE_IMAGE,
  USE_FOLDER_IMAGE,
  FONT_SCALE,
  FONT_COLOR,
  IMAGE_PADDING,
  BACKGROUND_BLUR,
  BACKGROUND_GROW,
  OUTPUT_PATH,
) = range(13)

DEFAULTS = {
  WIDTH: 1920,
  HEIGHT: 1080,
  BG_COLOR: "#000000",
  ENABLE_BG_IMAGE: False,
  USE_FILE_IMAGE: True,
  USE_FOLDER_IMAGE: True,
  FONT: None,
  FONT_SCALE: 0.8,
  FONT_COLOR: "#FFFFFF",
  IMAGE_PADDING: 0,
  BACKGROUND_BLUR: 10,
  BACKGROUND_GROW: 0.5,
  OUTPUT_PATH: Path.home() / __app_name__
}

class Config:
  """ Handles creating, modifying and reading the config.ini file."""
  def __init__(self, config_file_path: Path):
      self.width = DEFAULTS[WIDTH]
      self.height = DEFAULTS[HEIGHT]
      self.bg_color = DEFAULTS[BG_COLOR]
      self.font = DEFAULTS[FONT]
      self.font_scale = DEFAULTS[FONT_SCALE]
      self.font_color = DEFAULTS[FONT_COLOR]
      self.use_file_image = DEFAULTS[USE_FILE_IMAGE]
      self.use_folder_image = DEFAULTS[USE_FOLDER_IMAGE]
      self.image_padding = DEFAULTS[IMAGE_PADDING]
      self.enable_bg_image = DEFAULTS[ENABLE_BG_IMAGE]
      self.background_blur = DEFAULTS[BACKGROUND_BLUR]
      self.background_grow = DEFAULTS[BACKGROUND_GROW]
      self.output_path = DEFAULTS[OUTPUT_PATH]
      self.dimensions = (DEFAULTS[WIDTH], DEFAULTS[HEIGHT])
      self.read(config_file_path)
  
  def read(self, config_file_path):
    if Path.exists(config_file_path):
      parser = configparser.ConfigParser()
      parser.read(config_file_path)
      self.width = int(parser["General"]["width"])
      self.height = int(parser["General"]["height"])
      self.dimensions = (self.width, self.height)
      self.bg_color = parser["General"]["bg_color"]
      self.font = Path(parser["General"]["font"])
      self.font_scale = float(parser["General"]["font_scale"])
      self.font_color = parser["General"]["font_color"]
      self.image_padding = int(parser["General"]["image_padding"])
      self.use_file_image = parser["General"]["use_file_image"]
      self.use_folder_image = parser["General"]["use_folder_image"]
      self.output_path = Path(parser["General"]["output_path"])
      self.enable_bg_image = parser["General"]["enable_bg_image"]
      self.background_blur = int(parser["General"]["background_blur"])
      self.background_grow = float(parser["General"]["background_grow"])
    else:
      self.create_config_file(config_dir_path=config_file_path.parent, config_file_path=config_file_path)
      self.update(config_file_path)
    
  def update(self, config_file_path: Path):
    parser = configparser.ConfigParser()
    parser["General"] = {key: str(value) for key, value in vars(self).items()}
    try:
      with config_file_path.open("w") as file:
        parser.write(file)
    except OSError:
      return CONFIG_WRITE_ERROR
    return SUCCESS
  
  def create_config_file(self, config_dir_path: Path, config_file_path: Path) -> int:
    try:
      config_dir_path.mkdir(exist_ok=True)
    except OSError:
      return CONFIG_DIR_ERROR
    try:
      config_file_path.touch(exist_ok=True)
    except OSError:
      return CONFIG_FILE_ERROR
    return SUCCESS
  
  def remove_config_file(self, config_file_path: Path):
    """ Restores default configuration settings. """
    try:
      os.unlink(config_file_path)
    except OSError:
      return CONFIG_FILE_ERROR
    return SUCCESS


