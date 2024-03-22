import re
import pytest
from pathlib import Path
import tempfile

from mp3_to_mp4.utils import _valid_regex, clean_string, sort_track_list, valid_audio_file, valid_cover_name, valid_image_file


class TestUtils:
  def test_valid_regex(self):
    string = "hello"
    regex = re.compile(r"hello")
    assert _valid_regex(string, regex) == True
    assert _valid_regex("bouy", regex) == False
  def test_valid_audio_file(self):
    valid_audio_paths = [Path("audio.wav"), Path("audio.mp3"), Path("audio.aif"), Path("audio.aiff"), Path("audio.ogg"), Path("audio.FLAC")]
    assert all([valid_audio_file(path) for path in valid_audio_paths])
    invalid_audio_paths = [Path("image.jpeg"), Path("audio.mp3.mp4"), Path("flac")]
    assert all([True if valid_audio_file(path) == False else False for path in invalid_audio_paths])
  def test_valid_image_file(self):
    valid_image_paths = [Path("img.png"), Path("IMAGE.JPEG"), Path("pic.tiff"), Path("image.gif"), Path("image.jpg"), Path("jpg.JPEG")]
    assert all([valid_image_file(path) for path in valid_image_paths])
    invalid_image_paths = [Path("image.jrpg"), Path("audio.mp3.mp4"), Path("oops")]
    assert all([True if valid_image_file(path) == False else False for path in invalid_image_paths])
  def test_valid_cover_name(self):
    valid = [ 
      "folder.jpg", "folder.jpeg", 
      "folder.png", "albumart.jpeg", 
      "album_art.png", "Art.png",
      "aRT.jPeg" ]
    invalid = ["fulder.jp", "fol_.jpg", "folder.jpeg.png"]
    assert all([valid_cover_name(name) for name in valid])
    assert all([True for name in invalid if valid_cover_name(name) == False])
  def sort_track_list(self, temp_dir):
    paths = [Path(temp_dir / "1"), Path(temp_dir / "2"), Path(temp_dir / "3")]
    paths_scrambled = [Path(temp_dir / "3"), Path(temp_dir / "2"), Path(temp_dir / "1"), ]
    assert sort_track_list(paths_scrambled) == paths
  # def sort_track_list_not_by_filename(self):
  #   pass
  # def test_get_cover_image_list(self):
  #   pass
  # def test_get_audio_list(self, u: Utils):
  #   pass
  # def test_get_folder_list(self):
  #   pass
  def test_clean_string(self):
    test_string = "H11#23A!"
    clean = "H11-23A-"
    assert clean_string(string=test_string) == clean
