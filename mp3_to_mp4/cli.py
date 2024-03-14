""" This module provides the command line interface for mp3 to mp4 """
# mp3_to_mp4/cli.py
from pathlib import Path
from typing import Optional
from rich import print

import typer
from typing_extensions import Annotated

from mp3_to_mp4 import ERRORS, __app_name__, __version__, config as cfg, renderer

app = typer.Typer()

@app.command()
def config(
  bg_color: str = typer.Option(
    str(cfg.DEFAULT_VIDEO_BG_COLOR),
    "--bg-color",
    "-bg",
    prompt="Background Color? (Hex)",
  ),
  output_dir: str = typer.Option(
    str(cfg.DEFAULT_VIDEO_OUTPUT),
    "--output",
    "-o",
    prompt="Output directory?",
  ),
  width: int = typer.Option(
    int(cfg.DEFAULT_VIDEO_WIDTH),
    "--width",
    "-w",
    prompt="Video width: (px)"
  ),
  height: int = typer.Option(
    int(cfg.DEFAULT_VIDEO_HEIGHT),
    "--height",
    "-h",
    prompt="Video height: (px)"
  ),
  image_padding: int = typer.Option(
    int(cfg.DEFAULT_IMAGE_PADDING),
    "--padding",
    "-p",
    prompt="Image padding: (px)"
  ), 
) -> None:
  """
  Sets the default rendering configurations.
  """
  app_init_error = cfg.init_app(bg_color, output_dir, width, height, image_padding=image_padding)
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


@app.callback(invoke_without_command=True)
def main(
  version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show the application's version and exit.",
    callback=_version_callback,
    is_eager=True,
  ),
  path: Annotated[Path, typer.Option(
    exists=True,
    file_okay=True,
    dir_okay=True,
    readable=True
  )] = None,
  image: Annotated[Optional[Path], typer.Option(
    exists=True,
    file_okay=True,
    dir_okay=False,
    readable=True
    )] = None,
  join: bool = typer.Option(
    False,
    "--join",
    "-j",
    help="When using a folder, all tracks will be joined in sequence into a single video."
  )
) -> None:
  """
  Use --path to specify a file or a folder to process.
  An image can be specified with --image.
  """
  if path is not None:
    # Check for configuration
    cfg.check_config()
    # Get configuration
    render_cfg = cfg.RenderConfig(cfg.CONFIG_FILE_PATH)
    # get_config() Needs to be written
    video = renderer.Renderer(path=path, image=image, join=join, config=render_cfg)
    video.render()

