from pathlib import Path
from tinytag import TinyTag, TinyTagException
import re

class Utils:
  
  def _valid_path(self, str: str, regex: re) -> bool:
    if not regex.match(str):
      return False
    return True
  
  def valid_audio_file(self, path: Path) -> bool:
    audio_regex = re.compile(r"[.]wav$|[.]mp3$|[.]aiff?$|[.]ogg$|[.]flac", re.I)
    return self._valid_path(path.suffix, audio_regex)

  def valid_image_file(self, path: Path) -> bool:
    image_regex = re.compile(r"[.]png$|[.]jpe?g$|[.]tiff$|[.]gif$", re.I)
    return self._valid_path(path.suffix, image_regex)
  
  def valid_cover_name(self, filename: str) -> bool:
    img_re = re.compile(r"folder\.jpe?g|folder\.png|album_?art.jpe?g|album_?art.png|art.png|art.jpe?g", re.I)
    return self._valid_path(filename, img_re)
  
  def get_folder_list(self, path: Path, type_function) -> int:
    directory = path.iterdir()
    return [path for path in directory if type_function(path)]

  def sort_track_list(self, audio_list: list[Path], by_filename = True) -> list:
    if not by_filename:
      return sorted(audio_list, key=lambda audio: self.__get_track_disc_track_index(audio))
    return sorted(audio_list)
  
  def __get_track_disc_track_index(self, path: Path):
    try:
      tags = TinyTag.get(path)
      return int(tags.disc + tags.track)
    except TinyTagException:
      return path.name
  
  def get_cover_list(self, path: Path):
    return 

  
  def _clean_string(self, string: str):
    return re.sub(r"\W+", "-", string)
