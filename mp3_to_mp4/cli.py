""" This module provides the command line interface for mp3 to mp4 """
# mp3_to_mp4/cli.py
import os
from pathlib import Path
from typing import Optional
from rich import print
from rich.prompt import Prompt

import typer
from typing_extensions import Annotated

from mp3_to_mp4 import ERRORS, __app_name__, __version__, config as cfg, renderer

app = typer.Typer()

def _init_config():
  app_init_error = cfg.init_app(
    bg_color=cfg.DEFAULT_VIDEO_BG_COLOR,
    output_dir=cfg.DEFAULT_VIDEO_OUTPUT,
    width=cfg.DEFAULT_VIDEO_WIDTH,
    height=cfg.DEFAULT_VIDEO_HEIGHT,
    image_padding=cfg.DEFAULT_IMAGE_PADDING,
    sort_filename=cfg.DEFAULT_SORT)
  if app_init_error:
    print(
      f'Creating the config file failed with "{ERRORS[app_init_error]}',
      style="colors(9)"
    )
    raise typer.Exit(1)

if not os.path.isfile(cfg.CONFIG_FILE_PATH):
  _init_config()
  
user_cfg = cfg.RenderConfig(cfg.CONFIG_FILE_PATH)

@app.command()
def config(
  bg_color: str = typer.Option(
    str(user_cfg.bg_color),
    "--bg-color",
    "-bg",
    prompt="Background color? (Hex)"
  ),
  output_dir: str = typer.Option(
    str(user_cfg.output_dir),
    "--output",
    "-o",
    prompt="Output directory?",
  ),
  width: int = typer.Option(
    int(user_cfg.width),
    "--width",
    "-w",
    prompt="Video width? (px)"
  ),
  height: int = typer.Option(
    int(user_cfg.height),
    "--height",
    "-h",
    prompt="Video height? (px)"
  ),
  image_padding: int = typer.Option(
    int(user_cfg.image_padding),
    "--padding",
    "-p",
    prompt="Image padding? (px)"
  ),
  sort_filename: bool = typer.Option(
    bool(user_cfg.sort_filename),
    "--sort-filename",
    "-s",
    prompt="Prefer filenames for --join option sort:"
  )
) -> None:
  """
  Sets the default rendering configurations.
  """
  app_init_error = cfg.init_app(
    bg_color=bg_color,
    output_dir=output_dir,
    width=width,
    height=height,
    image_padding=image_padding,
    sort_filename=sort_filename)
  if app_init_error:
    print(
      f'Creating the config file failed with "{ERRORS[app_init_error]}',
      style="colors(9)"
    )
    raise typer.Exit(1)
  print(f"Configuration file written to: ", cfg.CONFIG_DIR_PATH)

@app.command()
def initconfig():
  """
  Sets the default rendering configurations.
  """
  _init_config()
  print("Configuration initialized to default settings.")

@app.command()
def convert(
    path: Annotated[Path, typer.Argument(
    exists=True,
    file_okay=True,
    dir_okay=True,
    readable=True,
    help="Specifies a path to a folder or file to convert."
  )] = None,
  image: Annotated[Optional[Path], typer.Option(
    exists=True,
    file_okay=True,
    dir_okay=False,
    readable=True,
    help="Specifies an image to use for conversions."
    )] = None,
  join: bool = typer.Option(
    False,
    "--join",
    "-j",
    help="When converting a folder, all tracks will be joined in sequence into a single video."
  ),
):
  """
  Converts a file or directory according to the config.
  """
  if path is not None:
    # get_config() Needs to be written
    video = renderer.Renderer(path=path, image=image, join=join, config=user_cfg)
    video.render()

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

