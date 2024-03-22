from pathlib import Path
from tinytag import TinyTag, TinyTagException
import re

class Utils:
  
  def _valid_regex(self, str: str, regex: re) -> bool:
    if not regex.match(str):
      return False
    return True
  
  def valid_audio_file(self, path: Path) -> bool:
    audio_regex = re.compile(r"[.]wav$|[.]mp3$|[.]aiff?$|[.]ogg$|[.]flac", re.I)
    return self._valid_regex(path.suffix, audio_regex)

  def valid_image_file(self, path: Path) -> bool:
    image_regex = re.compile(r"[.]png$|[.]jpe?g$|[.]tiff$|[.]gif$", re.I)
    return self._valid_regex(path.suffix, image_regex)
  
  def valid_cover_name(self, filename: str) -> bool:
    img_re = re.compile(r"folder\.jpe?g|folder\.png|album_?art.jpe?g|album_?art.png|art.png|art.jpe?g", re.I)
    return self._valid_regex(filename, img_re)

  def sort_track_list(self, audio_list: list[Path], by_filename = True) -> list:
    if not by_filename:
      return sorted(audio_list, key=lambda audio: self.__get_track_disc_track_index(audio))
    return sorted(audio_list)
  
  def __get_track_disc_track_index(self, path: Path):
    try:
      tags = TinyTag.get(path)
      return int(tags.disc + tags.track)
    except TinyTagException:
      return int(re.sub(r"-","", re.match(r"^\d{,2}-?\d{,2}", path.name).group(0)).strip("0"))
  
  def get_cover_image_list(self, path: Path):
    return self.get_folder_list(path, self.valid_cover_name)
  def get_audio_list(self, path: Path):
    return self.get_folder_list(path, self.valid_audio_file)
  
  def get_folder_list(self, path: Path, type_function) -> int:
    directory = path.iterdir()
    return [path for path in directory if type_function(path)]
  
  def clean_string(self, string: str):
    return re.sub(r"\W+", "-", string)

  # def check_params(self, bg_color: str, width: int, height: int):
  #   checks = [
  #   self.__check_color(bg_color),
  #   self.__check_dimension(width),
  #   self.__check_dimension(height),
  #   ]
  #   if all([True if check == SUCCESS else False for check in checks]):
  #     return SUCCESS
  #   return CONFIG_PARAM_ERROR

  # def __check_color(self, color: str):
  #   hex_regex = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
  #   if hex_regex.fullmatch(color) == None:
  #     return CONFIG_PARAM_ERROR
  #   return SUCCESS

  # def __check_dimension(self, px: int):
  #   if 0 < px < 3841:
  #     return SUCCESS
  #   return CONFIG_PARAM_ERROR
