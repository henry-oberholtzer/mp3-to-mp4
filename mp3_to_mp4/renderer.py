""" This module handles the video rendering functionality, based on MoviePy """

from pathlib import Path

import typer

from mp3_to_mp4 import __app_name__, SUCCESS, VIDEO_RENDER_ERROR, IMAGE_DIR_ERROR, IMAGE_FILE_ERROR, AUDIO_DIR_ERROR, AUDIO_FILE_ERROR, CONFIG_READ_ERROR

DEFAULT_VIDEO_BG_COLOR = "#000000"
DEFAULT_VIDEO_RES = (1920, 1080)
DEFAULT_VIDEO_FRAMERATE = 2
DEFAULT_VIDEO_OUTPUT = Path.home() / __app_name__

class Renderer:
  def __init__():
    pass

  def get_config() -> int:
    return SUCCESS

  def get_image() -> int:
    return SUCCESS
  
  def get_audio() -> int:
    return SUCCESS
  
