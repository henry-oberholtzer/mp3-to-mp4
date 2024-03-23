""" This module provides the command line interface for mp3 to mp4 """
# mp3_to_mp4/cli.py
from pathlib import Path
from typing import Optional
import typer
from typing_extensions import Annotated
from rich import print
from mp3_to_mp4.config import Config
from mp3_to_mp4.mp3_to_mp4 import Mp3ToMp4
from mp3_to_mp4 import ERRORS, SUCCESS, __app_name__, __version__

app = typer.Typer()

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

user_cfg = Config(config_file_path=CONFIG_FILE_PATH)

@app.command("config")
def set_config(
  show: bool = typer.Option(
    False,
    "--show",
    help="Prints the current configuration to the console."
  ),
  config_path: bool = typer.Option(
    False,
    "--path",
    help="Prints path to configuration file."
  ),
  init: bool = typer.Option(
    False,
    "--init",
    "-i",
    help="Initialize settings."
  ),
  output_path: Annotated[Optional[Path], typer.Option(
    exists=True,
    file_okay=False,
    dir_okay=True,
    help="Path for video output."
  )] = Path(user_cfg.output_path),
  width: int = typer.Option(
    int(user_cfg.width),
    "--width",
    "-w",
    help="Sets video width in pixels."
  ),
  height: int = typer.Option(
    int(user_cfg.height),
    "--height",
    "-h",
    help="Sets video height in pixels."
  ),
  image_padding: int = typer.Option(
    int(user_cfg.image_padding),
    "--padding",
    "-p",
    help="Padding for foreground image in pixels."
  ),
  bg_color: str = typer.Option(
    str(user_cfg.bg_color),
    "--bg-color",
    help="Hex code for background when not using image."
  ),
  use_file_image = typer.Option(
    bool(user_cfg.use_file_image),
    "--file-img",
    help="When enabled, checks file metadata for an image if none is supplied."
  ),
  use_folder_image = typer.Option(
    bool(user_cfg.use_folder_image),
    "--folder-image",
    help="When enabled, checks for a suitable image in the audio file's folder.",
  ),
  enable_bg_image: bool = typer.Option(
    bool(user_cfg.enable_bg_image),
    "--bg-img",
    help="Sets if background image will be used."
  ),
  background_blur: int = typer.Option(
    int(user_cfg.background_blur),
    "--bg-blur",
    help="Sets background image blur in pixels, 0 disables."
  ),
  background_grow: float = typer.Option(
    float(user_cfg.background_grow),
    "--bg-grow",
    help="Sets extra percentage to scale background image. Handy for enhancing offset when using album art."
  ),
  font: Annotated[Optional[Path], typer.Option(
    help="Path for font when an image cannot be found.",
  )] = user_cfg.font,
  font_color: str = typer.Option(
    str(user_cfg.font_color),
    "--font-color",
    help="Sets the hex code color for the font."
  ),
  font_scale: float = typer.Option(
    float(user_cfg.font_scale),
    "--font-scale",
    help="Sets the amount of screen the text width can take up, from 0.0 to 1.0."
    ),
) -> None:
  """
  Sets the configuration for convert.
  """
  if init:
    if (err := user_cfg.remove_config_file(CONFIG_FILE_PATH)) != SUCCESS:
      print(f'Removing the file failed with {ERRORS[err]}')
      raise typer.Exit(1)
    user_cfg.read(CONFIG_FILE_PATH)
    print(f"Configuration initialized.")
    raise typer.Exit()
  if config_path:
    print("Configuration file is located at:", CONFIG_FILE_PATH)
    raise typer.Exit()
  if show:
    print(vars(user_cfg))
    raise typer.Exit()
  else:
    # Update values.
    user_cfg.width = width
    user_cfg.height = height
    user_cfg.bg_color = bg_color
    user_cfg.font = font
    user_cfg.font_scale = font_scale
    user_cfg.font_color = font_color
    user_cfg.image_padding = image_padding
    user_cfg.use_file_image = use_file_image
    user_cfg.use_folder_image = use_folder_image
    user_cfg.output_path = output_path
    user_cfg.enable_bg_image = enable_bg_image
    user_cfg.background_blur = background_blur
    user_cfg.background_grow = background_grow
    if (err := user_cfg.update(CONFIG_FILE_PATH)) != SUCCESS:
      print(f'Updating the file failed with {ERRORS[err]}')
      raise typer.Exit(1)
    print(f"Configuration updated.")



@app.command()
def convert(
  path: Annotated[Optional[Path], typer.Argument(
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
  bg_image: Annotated[Optional[Path], typer.Option(
    exists=True,
    file_okay=True,
    dir_okay=False,
    readable=True,
    help="Sets a specific image for the background. Overrides enable background image."
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
    video = Mp3ToMp4(config=user_cfg, audio=path, image=image, bg_image=bg_image, join=join)
    # Create image from the image path.
  else:
    print("Please specify a target path or file.")

def _version_callback(value: bool) -> None:
  if value:
    print(f"{__app_name__} v{__version__}")
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

