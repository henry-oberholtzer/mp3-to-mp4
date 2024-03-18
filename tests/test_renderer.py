import os
from pathlib import Path
import tempfile
import pytest

from mp3_to_mp4 import config, renderer

r = renderer.Renderer

@pytest.fixture
def render(temp_user_cfg: config.Config, temp_dir):
  return r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)

class TestRenderer:
  def test_init(self, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    assert render.config == temp_user_cfg
    assert render.path == temp_dir
    assert render.image == temp_dir
    assert render.join == True
    assert render.audio_list == []
    assert render.dimensions == (temp_user_cfg.width, temp_user_cfg.height)
  def test_clean_string(self, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    test_string = "H11#23A!"
    clean = "H11-23A-"
    assert render._clean_string(string=test_string) == clean
  def test_sort_album_list(self, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    paths = [Path(temp_dir / "1"), Path(temp_dir / "2"), Path(temp_dir / "3")]
    paths_scrambled = [Path(temp_dir / "3"), Path(temp_dir / "2"), Path(temp_dir / "1"), ]
    render.audio_list = paths_scrambled
    assert render._sort_album_list() == paths
  def test_check_cover_filename(self, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    valid = [ 
      "folder.jpg", "folder.jpeg", 
      "folder.png", "albumart.jpeg", 
      "album_art.png", "Art.png",
      "aRT.jPeg" ]
    invalid = ["fulder.jp", "fol_.jpg", "folder.jpeg.png"]
    assert all([render._check_cover_filename(name) for name in valid])
    assert all([True for name in invalid if render._check_cover_filename(name) == False])
  def test_find_image_in_folder(self, monkeypatch, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    image_path = Path(temp_dir / "folder.jpg")
    monkeypatch.setattr(Path, "glob", lambda *args: [image_path])
    assert render._find_image_in_folder() == image_path
  def test_find_no_image_in_folder(self, monkeypatch, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    image_path = Path(temp_dir / "folder_art.jpg")
    monkeypatch.setattr(Path, "glob", lambda *args: [image_path])
    assert render._find_image_in_folder() == None
  def test_valid_audio(self, render: r):
    valid_audio_paths = [Path("audio.wav"), Path("audio.mp3"), Path("audio.aif"), Path("audio.aiff"), Path("audio.ogg"), Path("audio.FLAC")]
    assert all([render._valid_audio(path) for path in valid_audio_paths])
    invalid_audio_paths = [Path("image.jpeg"), Path("audio.mp3.mp4"), Path("flac")]
    assert all([True if render._valid_audio(path) == False else False for path in invalid_audio_paths])
  def test_valid_image(self, render: r):
    valid_image_paths = [Path("img.png"), Path("IMAGE.JPEG"), Path("pic.tiff"), Path("image.gif"), Path("image.jpg"), Path("jpg.JPEG")]
    assert all([render._valid_image(path) for path in valid_image_paths])
    invalid_image_paths = [Path("image.jrpg"), Path("audio.mp3.mp4"), Path("oops")]
    assert all([True if render._valid_image(path) == False else False for path in invalid_image_paths])
  def test_image_scale_dimensions(self, render: r):
    pass
