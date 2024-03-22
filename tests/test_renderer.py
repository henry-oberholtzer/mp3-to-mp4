# import io
# from tempfile import TemporaryFile
# import os
# from pathlib import Path
# from moviepy.video.VideoClip import ImageClip, TextClip
# import moviepy.audio.io.AudioFileClip as afc
# import PIL
# import pytest
# from tinytag import TinyTag
# import typer

# from mp3_to_mp4 import AUDIO_FILE_ERROR, SUCCESS, config, renderer

# r = renderer.Renderer

# @pytest.fixture
# def render(temp_user_cfg: config.Config, temp_dir):
#   return r(config=temp_user_cfg, path=temp_dir, image=temp_dir)

# def fake_folder_audio():
#   print("Appended Audio") 
#   return SUCCESS

# class FalseTags:
#   def __init__(self):
#     self.artist = "artist"
#     self.title = "title"
#     self.albumartist = "albumartist"
#     self.album = "album"
#   def get_image():
#     return "image".encode()

# class TestRenderer:
#   def test_init(self, temp_user_cfg: config.Config, temp_dir):
#     render = r(config=temp_user_cfg, path=temp_dir, image=temp_dir, join=True)
#     assert render.config == temp_user_cfg
#     assert render.path == temp_dir
#     assert render.image == temp_dir
#     assert render.join == True
#     assert render.audio_list == []
#     assert render.dimensions == (temp_user_cfg.width, temp_user_cfg.height)
#   def test_set_audio_list(self, temp_dir, monkeypatch, render: r):
#     monkeypatch.setattr(render, "_valid_audio", lambda path: True)
#     render._set_audio_list()
#     assert render.audio_list == [render.path]
    
#   def test_set_audio_list_path_is_dir(self, monkeypatch, capsys, render: r):
#     monkeypatch.setattr(render, "_get_folder_audio", fake_folder_audio)
#     render.render()
#     captured = capsys.readouterr()
#     assert captured.out == "Appended Audio\n"
    
#   def test_set_audio_list_no_audio(self, capsys, render: r):
#     with pytest.raises(typer.Exit):
#       render._set_audio_list()
#     captured = capsys.readouterr()
#     assert render.audio_list == []
#     assert captured.out == f"No viable audio files available in directory. Aborting.\n"
#   def test_render_join_false(self, monkeypatch, mocker, render: r):
#     monkeypatch.setattr(render, "_set_audio_list", lambda: None)
#     monkeypatch.setattr(render, "_render_album", lambda: None)
#     monkeypatch.setattr(render, "_render_batch", lambda: None)
#     spy = mocker.spy(render, '_set_audio_list')
#     spy_album = mocker.spy(render, '_render_album')
#     spy_batch = mocker.spy(render, '_render_batch')
#     render.render()
#     assert spy.call_count == 1
#     assert spy_album.call_count == 0
#     assert spy_batch.call_count == 1

#   def test_render_join_true(self, monkeypatch, mocker, render: r):
#     monkeypatch.setattr(render, "_set_audio_list", lambda: None)
#     monkeypatch.setattr(render, "_render_album", lambda: None)
#     monkeypatch.setattr(render, "_render_batch", lambda: None)
#     spy = mocker.spy(render, '_set_audio_list')
#     spy_album = mocker.spy(render, '_render_album')
#     spy_batch = mocker.spy(render, '_render_batch')
#     render.join = True
#     render.render()
#     assert spy.call_count == 1
#     assert spy_album.call_count == 1
#     assert spy_batch.call_count == 0
    
#   # def test_final_render(self, render: r):
#   #   pass
#   # def test_render_batch(self, temp_mp3, monkeypatch, render: r):
#   #     render.audio_list = [Path(temp_mp3.name)]
#   #     monkeypatch.setattr(render, "_create_image", lambda args: True)
#   #     monkeypatch.setattr(render, "_final_render", lambda **kwargs: True)
#   #     monkeypatch.setattr(afc, "AudioFileClip", lambda **kwargs: True)
#   #     render._render_batch()
#   # def test_render_album(self, render: r):
#   #   pass
#   # def test_create_file_name(self, render: r):
#   #   pass
#   # def test_close_render(self, render: r):
#   #   pass

# class falsePath:
#   def __init__(self, paths):
#     self.paths = paths
#   def iterdir(self):
#     return self.paths

