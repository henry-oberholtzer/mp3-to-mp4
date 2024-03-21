import io
import py
import os
from pathlib import Path
from moviepy.video.VideoClip import ImageClip, TextClip
import PIL
import pytest
from tinytag import TinyTag
import typer

from mp3_to_mp4 import SUCCESS, config, renderer

r = renderer.Renderer

@pytest.fixture
def render(temp_user_cfg: config.Config, temp_dir):
  return r(config=temp_user_cfg, path=temp_dir, image=temp_dir)

def fake_folder_audio():
  print("Appended Audio") 
  return SUCCESS

class FalseTags:
  def __init__(self):
    self.artist = "artist"
    self.title = "title"
    self.albumartist = "albumartist"
    self.album = "album"
  def get_image():
    return "image".encode()

class TestRenderer:
  def test_init(self, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    assert render.config == temp_user_cfg
    assert render.path == temp_dir
    assert render.image == temp_dir
    assert render.join == True
    assert render.audio_list == []
    assert render.dimensions == (temp_user_cfg.width, temp_user_cfg.height)
  def test_set_audio_list(self, temp_dir, monkeypatch, render: r):
    monkeypatch.setattr(render, "_valid_audio", lambda path: True)
    render._set_audio_list()
    assert render.audio_list == [render.path]
    
  def test_set_audio_list_path_is_dir(self, monkeypatch, capsys, render: r):
    monkeypatch.setattr(render, "_get_folder_audio", fake_folder_audio)
    render.render()
    captured = capsys.readouterr()
    assert captured.out == "Appended Audio\n"
    
  def test_set_audio_list_no_audio(self, capsys, render: r):
    with pytest.raises(typer.Exit):
      render._set_audio_list()
    captured = capsys.readouterr()
    assert render.audio_list == []
    assert captured.out == f"No viable audio files available in directory. Aborting.\n"
  def test_render_join_false(self, monkeypatch, mocker, render: r):
    monkeypatch.setattr(render, "_set_audio_list", lambda: None)
    monkeypatch.setattr(render, "_render_album", lambda: None)
    monkeypatch.setattr(render, "_render_batch", lambda: None)
    spy = mocker.spy(render, '_set_audio_list')
    spy_album = mocker.spy(render, '_render_album')
    spy_batch = mocker.spy(render, '_render_batch')
    render.render()
    assert spy.call_count == 1
    assert spy_album.call_count == 0
    assert spy_batch.call_count == 1

  def test_render_join_true(self, monkeypatch, mocker, render: r):
    monkeypatch.setattr(render, "_set_audio_list", lambda: None)
    monkeypatch.setattr(render, "_render_album", lambda: None)
    monkeypatch.setattr(render, "_render_batch", lambda: None)
    spy = mocker.spy(render, '_set_audio_list')
    spy_album = mocker.spy(render, '_render_album')
    spy_batch = mocker.spy(render, '_render_batch')
    render.join = True
    render.render()
    assert spy.call_count == 1
    assert spy_album.call_count == 1
    assert spy_batch.call_count == 0
    
  def test_final_render(self, render: r):
    pass
  
  def test_render_batch(self, render: r):
    pass

  def test_render_album(self, render: r):
    pass
  def test_create_file_name(self, render: r):
    pass
  
  def test_close_render(self, render: r):
    pass


class TestRendererFileFunctions:
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
  def test_get_folder_audio(self, render: r):
    pytest.fail("Not written")
  def test_sort_album_list(self, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    paths = [Path(temp_dir / "1"), Path(temp_dir / "2"), Path(temp_dir / "3")]
    paths_scrambled = [Path(temp_dir / "3"), Path(temp_dir / "2"), Path(temp_dir / "1"), ]
    render.audio_list = paths_scrambled
    assert render._sort_album_list() == paths
  def test_sort_album_list_by_tags(self, mocker, render: r):
    render.config.sort_filename = False
    assert render._sort_album_list() == []
    
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
  def test_clean_string(self, temp_user_cfg: config.Config, temp_dir):
    render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
    test_string = "H11#23A!"
    clean = "H11-23A-"
    assert render._clean_string(string=test_string) == clean

class TestRendererImageFunctions:
  def test_image_scale_dimensions(self, render: r):
    render.config.height = 400
    render.config.width = 600
    scale = render._image_scale_dimensions((300, 300))
    assert scale == (400, 400)
  def test_image_scale_padding(self, render: r):
    render.config.image_padding = 50
    render.config.height = 300
    render.config.width = 300
    scale = render._image_scale_dimensions((300, 300))
    assert scale == (200, 200)
  def test_image_scale_padding_oversize(self, render: r):
    render.config.image_padding = 350
    render.config.height = 300
    render.config.width = 300
    scale = render._image_scale_dimensions((300, 300))
    assert scale == (200, 200)
  def test_image_hex_to_rgb(self, render: r):
    hex_rgb_pairs = [("#000", (0,0,0)), ("#FFFFFF", (255, 255, 255)), ("#FF00FF", (255, 0, 255))]
    for hex, rgb in hex_rgb_pairs:
      assert render._image_hex_to_rgb(hex) == rgb
  def test_image_resize(self, render: r):
    temp_image = PIL.Image.new(mode="RGB", size=(200, 200))
    temp_image_path = Path(render.config.config_dir_path / "image.jpg")
    temp_image.save(temp_image_path)
    assert isinstance(render._image_resize(temp_image_path), PIL.Image.Image)
  def test_image_clip_on_color(self, monkeypatch, render: r):
    temp_image = PIL.Image.new(mode="RGB", size=(200, 200))
    temp_image_path = os.path.join(render.config.config_dir_path, "first_image.jpeg")
    temp_image.save(temp_image_path)
    filepath = os.path.join(render.config.config_dir_path / "second_image.png")
    with render._image_clip_on_color(temp_image_path, filepath) as image_clip_on_color:
      assert os.path.isfile(filepath)
      assert os.path.isfile(temp_image_path)
      assert isinstance(image_clip_on_color, ImageClip)
  def test_image_text_on_color(self, render: r):
    tags = FalseTags()
    result = render._image_text_on_color(tags)
    assert isinstance(result, ImageClip)
    assert result.size == render.dimensions
  def test_image_text_on_color_join(self, render: r):
    tags = FalseTags()
    render.join = True
    result = render._image_text_on_color(tags)
    assert isinstance(result, ImageClip)
    assert result.size == render.dimensions
  def test_create_image_provided_image(self, monkeypatch, render: r):
    monkeypatch.setattr(TinyTag, "get", lambda path, image: FalseTags)
    monkeypatch.setattr(render, "_image_clip_on_color", lambda image, filepath: True)
    assert render.image is not None
    assert render._create_image(render.config.config_file_path) == True
  def test_create_image_metadata_image(self, monkeypatch, render: r):
    monkeypatch.setattr(TinyTag, "get", lambda path, image: FalseTags)
    monkeypatch.setattr(render, "_image_clip_on_color", lambda image, filepath: True)
    render.image = None
    assert render.image is None
    assert render._create_image(render.config.config_file_path) == True
  def test_create_image_folder_image(self, monkeypatch, render: r):
    monkeypatch.setattr(TinyTag, "get", lambda path, image: FalseTags)
    monkeypatch.setattr(FalseTags, "get_image", lambda: None)
    monkeypatch.setattr(render, "_image_clip_on_color", lambda image, filepath: True)
    monkeypatch.setattr(render, "_find_image_in_folder", lambda: True)
    render.image = None
    assert render.image is None
    assert FalseTags.get_image() == None
    assert render._find_image_in_folder() == True
    assert render._create_image(render.config.config_file_path) == True
  def test_create_image_no_image(self, mocker, monkeypatch, render: r):
    monkeypatch.setattr(TinyTag, "get", lambda path, image: FalseTags)
    monkeypatch.setattr(FalseTags, "get_image", lambda: None)
    render.image = None
    monkeypatch.setattr(render, "_find_image_in_folder", lambda: None)
    monkeypatch.setattr(render, "_image_text_on_color", lambda tags: True)
    spy = mocker.spy(render, '_image_text_on_color')
    assert render._create_image(render.config.config_file_path) == True
    assert spy.call_count == 1
