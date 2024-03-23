from pathlib import Path
import re


def _valid_regex(str: str, regex: re) -> bool:
  if not regex.match(str):
    return False
  return True
  
def valid_audio_file(path: Path) -> bool:
  audio_regex = re.compile(r"[.]wav$|[.]mp3$|[.]aiff?$|[.]ogg$|[.]flac", re.I)
  return _valid_regex(path.suffix, audio_regex)

def valid_image_file(path: Path) -> bool:
  image_regex = re.compile(r"[.]png$|[.]jpe?g$|[.]tiff$|[.]gif$", re.I)
  return _valid_regex(path.suffix, image_regex)
  
def valid_cover_name(filename: str) -> bool:
  img_re = re.compile(r"folder\.jpe?g|folder\.png|album_?art.jpe?g|album_?art.png|art.png|art.jpe?g", re.I)
  return _valid_regex(filename, img_re)

def get_cover_image_list(path: Path) -> list[Path]:
  return get_folder_list(path, valid_cover_name)
  
def get_audio_list(path: Path) -> list[Path]:
    return get_folder_list(path, valid_audio_file)
  
def get_folder_list(path: Path, type_function) -> int:
  directory = path.iterdir()
  return [path for path in directory if type_function(path)]
  
def clean_string(string: str):
  return re.sub(r"\W+", "-", string)
