""" This module handles the video rendering functionality, based on MoviePy """

from pathlib import Path

import typer

from mp3_to_mp4 import __app_name__

DEFAULT_VIDEO_BG_COLOR = "#000000"
DEFAULT_VIDEO_RES = (1920, 1080)
DEFAULT_VIDEO_FRAMERATE = 2
DEFAULT_VIDEO_OUTPUT = Path(typer.get_app_dir(__app_name__))
