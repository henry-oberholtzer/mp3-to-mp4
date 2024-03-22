""" This module provides the command line interface for mp3 to mp4 """
# mp3_to_mp4/cli.py
from pathlib import Path
from typing import Optional
import typer
from typing_extensions import Annotated

from mp3_to_mp4.config import Config
from mp3_to_mp4.mp3_to_mp4 import Mp3ToMp4
from mp3_to_mp4 import ERRORS, SUCCESS, __app_name__, __version__, renderer

app = typer.Typer()

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

user_cfg = Config(config_file_path=CONFIG_FILE_PATH)

@app.command("config")
def set_config(
  init: bool = typer.Option(
    False,
    "--init",
    "-i",
    help="Initialize settings."
  ),
  bg_color: str = typer.Option(
    str(user_cfg.bg_color),
    "--bg-color",
    "-bg",
  ),
  output_path: Annotated[Optional[Path], typer.Option(
    exists=True,
    file_okay=False,
    dir_okay=True
  )] = Path(user_cfg.output_path),
  width: int = typer.Option(
    int(user_cfg.width),
    "--width",
    "-w",
  ),
  height: int = typer.Option(
    int(user_cfg.height),
    "--height",
    "-h",
  ),
  image_padding: int = typer.Option(
    int(user_cfg.image_padding),
    "--padding",
    "-p",
  ),
) -> None:
  """
  Sets the configuration for convert.
  """
  if init:
    if (err := user_cfg.remove_config_file()) != SUCCESS:
      print(f'Removing the file failed with {ERRORS[err]}')
      raise typer.Exit(1)
    user_cfg.read(CONFIG_FILE_PATH)
    print(f"Configuration initialized.")
  else:
    # Update values.
    return



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
    video = Mp3ToMp4(config=user_cfg, audio=path, image=image, join=join)
    # Create image from the image path.
    if (err:= video.build_image()) != SUCCESS:
      print(f"Creating the image failed with {ERRORS[err]}")
      video.close()
      raise typer.Exit(1)
    print("Image built.")
    if (err:= video.build_audio()) != SUCCESS:
      print(f"Creating the audio failed with {ERRORS[err]}")
      video.close()
      raise typer.Exit(1)
    print("Audio built.")
    if (err:= video.render()) != SUCCESS:
      print(f"Rendering the video failed with {ERRORS[err]}")
      video.close()
      raise typer.Exit(1)
    video.close()
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

