""" This module handles the video rendering functionality, based on MoviePy """
import io
import re
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips
from moviepy.video.compositing import CompositeVideoClip
from tinytag import TinyTag
from PIL import Image
from PIL.Image import Resampling
from rich import print


from pathlib import Path

import typer

from mp3_to_mp4 import (__app_name__, ERRORS, SUCCESS, VIDEO_RENDER_ERROR, 
  IMAGE_FILE_ERROR, AUDIO_FILE_ERROR, config)

class Renderer:
  def __init__(self, config: config.RenderConfig, path: Path, image: Path = None, join: bool = False):
    self.config = config
    self.path = path
    self.image = image
    self.join = join
    self.audio_list = []
    self.dimensions = (self.config.width, self.config.height)
    
  def render(self):
    # If the path is a file, proceed with single file rendering.
    if self.image is not None and self.image.is_file():
        # Rendering with provided image
        print(self.image)
    if self.path.is_file():
      # Rendering without provided image
      if self._valid_audio(self.path):
        self.audio_list.append(self.path)
      else:
        return AUDIO_FILE_ERROR
    elif self.path.is_dir():
      # If path is a directory, get all the files in the folder.
      self._get_folder_audio()
    if len(self.audio_list) == 0:
      print(
      f"No viable audio files available in directory. Aborting.")
      raise typer.Exit(1)
    # Now that the audio lists have been compiled, proceed to render all items in audio list.
    if self.join == False:
      self._render_batch()
    else:
      self._render_album()
  
  def _render_batch(self):
    for audio in self.audio_list:
      # Generate background image.
      image: CompositeVideoClip = self._create_image(audio)
      # Add audio to composite video clip.
      audio_clip = AudioFileClip(str(audio))
      image.duration = audio_clip.duration
      image.audio = audio_clip
      # Make filename.
      tags = TinyTag.get(audio)
      filename = self._clean_string(f"{tags.track}-{tags.artist}-{tags.title}")
      # Render.
      self._final_render(image, self.config.output_dir, filename)
      # Close & remove files.
      image.close()
      audio_clip.close()
      if Path('temp_art.png').is_file():
        Path('temp_art.png').unlink()
  
  def _render_album(self):
    sorted = self._sort_album_list()
    audio_compile = concatenate_audioclips([AudioFileClip(str(file)) for file in sorted])
    image: CompositeVideoClip = self._create_image(self.audio_list[0])
    image.duration = audio_compile.duration
    image.audio = audio_compile
    # Make filename
    tags = TinyTag.get(self.audio_list[0])
    filename = self._clean_string(f"{tags.albumartist}-{tags.album}")
    self._final_render(image, self.config.output_dir, filename)
    image.close()
    audio_compile.close()
    if Path('temp_art.png').is_file():
        Path('temp_art.png').unlink()
  
  def _final_render(self, clip: CompositeVideoClip, output_dir: str, filename: str):
    Path(output_dir).mkdir(exist_ok=True)
    clip.write_videofile(filename=f"{output_dir}\\{filename}.mp4", fps=self.config.output_fps, codec="libx264", audio_bitrate="320k", ffmpeg_params=['-tune','stillimage'])

  def _valid_path(self, path: Path, regex: re, err: int) -> bool:
    if not regex.match(path.suffix):
      return False
    return True
  
  def _valid_audio(self, path: Path):
    audio_regex = re.compile("[.]wav$|[.]mp3$|[.]aiff?$|[.]ogg$|[.]flac", re.I)
    return self._valid_path(path, audio_regex, AUDIO_FILE_ERROR)

  def _valid_image(self, path: Path):
    image_regex = re.compile("[.]png$|[.]jpe?g$|[.]tiff$|[.]gif$")
    return self._valid_path(path, image_regex, IMAGE_FILE_ERROR)
  
  def _get_folder_audio(self) -> int:
    directory = self.path.glob("*.*")
    self.audio_list = [path for path in directory if self._valid_audio(path)]
    if not len(self.audio_list) > 0:
      return AUDIO_FILE_ERROR
    return SUCCESS
  
  def _hex_to_rgb(self, hex: str) -> tuple:
    h = hex.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
  
  def _get_image_from_bytes(self, image: bytes):
    pi = Image.open(io.BytesIO(image))
    resize = pi.resize(self._resize_dimensions(pi.size), resample=Resampling.LANCZOS)
    resize.save('temp_art.png')
    return 'temp_art.png'
  
  def _resize_dimensions(self, dimensions: tuple[int, int]) -> tuple:
    w, h = dimensions
    new_width = int(w * (self.config.height/h)) - (2*self.config.image_padding)
    new_height = int(self.config.height - (2*self.config.image_padding))
    return (new_width, new_height)
  
  def _create_image(self, current_audio: Path):
    tags = TinyTag.get(current_audio, image=True)
    color = self._hex_to_rgb(self.config.bg_color)
    image_bytes = tags.get_image()
    # Grabs image from directory.
    if self.image is not None:
      pi = Image.open(self.image)
      resize = pi.resize(self._resize_dimensions(pi.size), resample=Resampling.LANCZOS)
      resize.save('temp_art.png')
      image = ImageClip('temp_art.png')
      return image.on_color(size=self.dimensions, color=color)
    # Grabs image from metadata.
    elif image_bytes is not None:
      image_path = self._get_image_from_bytes(image_bytes)
      image = ImageClip(image_path)
      return image.on_color(size=self.dimensions, color=color)
    # Will eventually handle rendering without an image provided.
    elif (folder_image := self._find_image_in_folder()) is not None:
      pi = Image.open(folder_image)
      resize = pi.resize(self._resize_dimensions(pi.size), resample=Resampling.LANCZOS)
      resize.save('temp_art.png')
      image = ImageClip('temp_art.png')
      return image.on_color(size=self.dimensions, color=color)
    text = TextClip(txt=f"{tags.artist}\n{tags.title}", font='Courier', color='white', size=self.dimensions)
    if self.join:
      text = TextClip(txt=f"{tags.albumartist}\n{tags.album}", font='Courier', color='white', size=self.dimensions)
    return text.on_color(size=self.dimensions, color=color)

  def _clean_string(self, string: str):
    return re.sub(r"\W+", "-", string)

  def _sort_album_list(self) -> list:
    if not self.config.sort_filename:
      return sorted(self.audio_list, key=lambda audio: int(TinyTag.get(audio).disc + TinyTag.get(audio).track))
    return sorted(self.audio_list)
  
  def _find_image_in_folder(self) -> Path:
    directory = self.path.glob("*.*")
    possible_images = re.compile(r"folder\.jpe?g|folder\.png|album_?art.jpe?g|album_?art.png|art.png|art.jpe?g", re.I)
    image_options = [obj for obj in directory if possible_images.match(obj.name)]
    if len(image_options) != 0:
      return image_options[0]
    return None
