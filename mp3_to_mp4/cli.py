""" This module provides the command line interface for mp3 to mp4 """
# mp3_to_mp4/cli.py
from pathlib import Path
from typing import Optional
from rich import print

import typer

from mp3_to_mp4 import ERRORS, __app_name__, __version__, config, renderer

app = typer.Typer()

@app.command()
def init(
  bg_color: str = typer.Option(
    str(renderer.DEFAULT_VIDEO_BG_COLOR),
    "--bg-color",
    "-bgc",
    prompt=f"Background Color? (Hex)",
  ),
) -> None:
  """
  Sets the default rendering configuration.
  """
  app_init_error = config.init_app(bg_color)
  if app_init_error:
    print(
      f'Creating the config file failed with "{ERRORS[app_init_error]}',
      style="colors(9)"
    )
    raise typer.Exit(1)

def _version_callback(value: bool) -> None:
  if value:
    print(f"{__app_name__} v{__version__}\n")
    raise typer.Exit()

@app.callback()
def main(
  version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show the application's version and exit.",
    callback=_version_callback,
    is_eager=True,
  )
) -> None:
  return




@app.command()
def render(audio: str, image: str = None):
  """
  Requires a specification of the path to the --audio
  
  Optionally accepts an --image to use for the mp4.
  
  Renders based on default configurations, unless arguments are supplied explicity.
  """
  typer.echo(f"Converting: {audio}")
  if image != None:
    typer.echo(f"Using Image: {image}")

@app.command()
def batch_render(directory: str, image: str = None, as_full_album: bool = False):
  """
  Renders a selected --directory into mp4 videos
  
  All valid audio files in the directory can be combined into one video with --as-full-album
  
  If --image is specified, the image will be used for every mp4 rendered.
  """
