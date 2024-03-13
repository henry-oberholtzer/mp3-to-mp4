""" This module provides the command line interface for mp3 to mp4 """
# mp3_to_mp4/cli.py
from pathlib import Path
from typing import Optional
from rich import print

import typer
from typing_extensions import Annotated

from mp3_to_mp4 import ERRORS, __app_name__, __version__, config, renderer

app = typer.Typer()

@app.command()
def configure(
  bg_color: str = typer.Option(
    str(renderer.DEFAULT_VIDEO_BG_COLOR),
    "--bg-color",
    "-bg",
    prompt=f"Background Color? (Hex)",
  ),
  output_dir: str = typer.Option(
    str(renderer.DEFAULT_VIDEO_OUTPUT),
    "--output",
    "-o",
    prompt=f"Output directory?",
  ),
) -> None:
  """
  Sets the default rendering configurationspoetr.
  """
  app_init_error = config.init_app(bg_color, output_dir)
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
  ),
) -> None:
  """
  A specific file to convert can be specified with --audio.
  An image to use can be specified with --image.
  A folder to process can be specified with --folder.
  """
  
  return

@app.command()
def render(
    image: Annotated[Optional[Path], typer.Option(
    exists=True,
    file_okay=True,
    dir_okay=False,
    readable=True
    )] = None,
  audio: Annotated[Optional[Path], typer.Option(
    exists=True,
    file_okay=True,
    dir_okay=False,
    readable=True
  )] = None,
  folder: Annotated[Optional[Path], typer.Option(
    exists=True,
    file_okay=False,
    dir_okay=True,
    readable=True
  )] = None,
  join: bool = typer.Option(
    False,
    "--join",
    "-j",
    help="When using a folder, all tracks will be join in sequence into a single video."
  )):
  """
  Requires a path to an audio file for the --audio paramter.
  Optionally accepts an --image to use for the mp4.
  Renders based on default configurations, unless arguments are supplied explicity.
  """
  # If no folder, render a single track
  if folder is None:
    if audio is not None:
      print(f"Using audio: {audio}")
    if image is not None:
      print(image)
  else:
  # If a folder is specified, render a batch of tracks.
    print(folder)
    if join is not False:
      print(f"Joining tracks.")
    if image is not None:
      print(image)
