""" This module handles the video rendering functionality, based on MoviePy """
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.fx.resize import resize
from moviepy.video.compositing import CompositeVideoClip
from rich import print
import configparser
import os


from pathlib import Path

import typer

from mp3_to_mp4 import (__app_name__, SUCCESS, ERRORS, VIDEO_RENDER_ERROR, IMAGE_DIR_ERROR, 
  IMAGE_FILE_ERROR, AUDIO_DIR_ERROR, AUDIO_FILE_ERROR, CONFIG_READ_ERROR)
from config import CONFIG_FILE_PATH, init_app

DEFAULT_VIDEO_BG_COLOR = "#000000"
DEFAULT_VIDEO_HEIGHT = 1080
DEFAULT_VIDEO_WIDTH = 1920
DEFAULT_VIDEO_FRAMERATE = 2
DEFAULT_VIDEO_OUTPUT = Path.home() / __app_name__

class Renderer:
  def __init__(self):
    self.height = DEFAULT_VIDEO_WIDTH
    self.width = DEFAULT_VIDEO_HEIGHT
    self.fps = DEFAULT_VIDEO_FRAMERATE
    self.output_path = DEFAULT_VIDEO_OUTPUT


  def _get_config() -> int:
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
  
  def render(self, clip: CompositeVideoClip):
    clip.write_videofile(filename=f"{self.output_folder}/{clean_file_name}.mp4", fps=2, codec="libx264")

  def get_image() -> int:
    return SUCCESS
  
  def get_audio() -> int:
    return SUCCESS
  
