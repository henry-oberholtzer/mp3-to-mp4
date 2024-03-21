""" This module handles the video rendering functionality, based on MoviePy """
import re
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips
from tinytag import TinyTag
from pathlib import Path
from PIL import Image, ImageColor

import typer

from mp3_to_mp4 import (__app_name__, SUCCESS, AUDIO_FILE_ERROR, config)
from mp3_to_mp4.create_image import CreateImage

class Renderer:
  def __init__(self, config: config.Config, path: Path, image: Path = None, join: bool = False):
    self.config = config
    self.path = path
    self.image = image
    self.join = join
    self.audio_list = []
    self.dimensions = (self.config.width, self.config.height)

# This chunk is concerned with actually rendering the video.

  def render(self):
    self._set_audio_list()
    # Now that the audio lists have been compiled, proceed to render all items in audio list.
    if self.join:
      return self._render_album()
    # If the path is a file, proceed with single file rendering.
    return self._render_batch()
      
  def _set_audio_list(self):
    if self._valid_audio(self.path):
      self.audio_list.append(self.path)
    elif self.path.is_dir():
    # If path is a directory, get all the files in the folder.
      folder_audio = self._get_folder_audio()
      if folder_audio != SUCCESS:
        print(f"No viable audio files available in directory. Aborting.")
        raise typer.Exit(1)
  
  def _render_batch(self):
    for audio in self.audio_list:
      self._final_render(
      clip=self._create_image(audio), 
      audio=AudioFileClip(str(audio)), 
      filename=self._create_file_name(audio))
  
  def _render_album(self):
    self._sort_album_list()
    self._final_render(
      clip=self._create_image(self.audio_list[0]), 
      audio=concatenate_audioclips([AudioFileClip(str(file)) for file in sorted]),
      filename=self._create_file_name(self.audio_list[0], album=True))
    
  def _create_file_name(self, audio: Path, album: bool = False) -> str:
    tags = TinyTag.get(audio)
    if album:
      return self._clean_string(f"{tags.albumartist}-{tags.album}")
    return self._clean_string(f"{tags.track}-{tags.artist}-{tags.title}")
  
  def _close_render(self, image: ImageClip, audio: AudioFileClip) -> int:
    image.close()
    audio.close()
    if Path('temp_art.png').is_file():
        Path('temp_art.png').unlink()
    return SUCCESS
  
  def _final_render(self, clip: ImageClip, audio: AudioFileClip, filename: str):
    clip.duration = audio.duration
    clip.audio = audio
    Path(self.config.output_dir).mkdir(exist_ok=True)
    clip.write_videofile(filename=f"{self.config.output_dir}\\{filename}.mp4", fps=self.config.output_fps, codec="libx264", audio_bitrate="320k", ffmpeg_params=['-tune','stillimage'])
    self._close_render(clip, audio)

# This chunk is primarily concerned with finding the appropriate files, so I may also split this off.
  def _valid_path(self, path: Path, regex: re) -> bool:
    if not regex.match(path.suffix):
      return False
    return True
  
  def _valid_audio(self, path: Path):
    audio_regex = re.compile(r"[.]wav$|[.]mp3$|[.]aiff?$|[.]ogg$|[.]flac", re.I)
    return self._valid_path(path, audio_regex)

  def _valid_image(self, path: Path):
    image_regex = re.compile(r"[.]png$|[.]jpe?g$|[.]tiff$|[.]gif$", re.I)
    return self._valid_path(path, image_regex)
  
  def _get_folder_audio(self) -> int:
    directory = self.path.iterdir()
    self.audio_list = [path for path in directory if self._valid_audio(path)]
    if not len(self.audio_list) > 0:
      return AUDIO_FILE_ERROR
    return SUCCESS
  
  def _sort_album_list(self) -> list:
    if not self.config.sort_filename:
      return sorted(self.audio_list, key=lambda audio: int(TinyTag.get(audio).disc + TinyTag.get(audio).track))
    return sorted(self.audio_list)
  
  def _check_cover_filename(self, filename: str) -> bool:
    img_re = re.compile(r"folder\.jpe?g|folder\.png|album_?art.jpe?g|album_?art.png|art.png|art.jpe?g", re.I)
    if img_re.fullmatch(filename):
      return True
    return False
    
  def _find_image_in_folder(self) -> Path:
    directory = self.path.glob("*.*")
    image_options = [obj for obj in directory if self._check_cover_filename(obj.name)]
    if len(image_options) != 0:
      return image_options[0]
    return None
  
  def _clean_string(self, string: str):
    return re.sub(r"\W+", "-", string)

# This chunk is purely concerned with image things, so I may split this off soon.
  
  def create_image(self) -> Image:
    ci = CreateImage(
      color=ImageColor(self.config.bg_color)
    )
    if self.image:
      ci.foreground = Image.open(self.image)
    
    
    
    return ci.composite_image()

  
