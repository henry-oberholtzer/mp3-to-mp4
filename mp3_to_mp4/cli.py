""" This module provides the command line interface for mp3 to mp4 """
# mp3_to_mp4/cli.py

from typing import Optional

import typer

from mp3_to_mp4 import __app_name__, __version__

app = typer.Typer()

def _version_callback(value: bool) -> None:
  if value:
    typer.echo(f"{__app_name__} v{__version__}\n")
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
def config():
  """
  Sets the rendering configuration.
  """

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
