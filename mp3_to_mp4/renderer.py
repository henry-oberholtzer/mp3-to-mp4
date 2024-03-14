""" This module handles the video rendering functionality, based on MoviePy """
import io
import re
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.fx.resize import resize
from moviepy.video.compositing import CompositeVideoClip
from tinytag import TinyTag
from PIL import Image
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
    else:
      print(
      f'Creating the config file failed with "{ERRORS[VIDEO_RENDER_ERROR]}',
      style="colors(9)"
    )
      raise typer.Exit(1)
    # Now that the audio lists have been compiled, proceed to render all items in audio list.
    for audio in self.audio_list:
      print(audio)
      # Generate background image.
      image: CompositeVideoClip = self._create_image(audio)
      # Composite with art.
    
      # Add audio to composite video clip.
      audio_clip = AudioFileClip(str(audio))
      image.duration = audio_clip.duration
      image.audio = audio_clip
      # Make filename.
      tags = TinyTag.get(audio, image=True)
      filename = self._clean_string(f"{tags.track}-{tags.artist}-{tags.title}")
      # Render.
      self._final_render(image, self.config.output_dir, filename)
      # Close & remove files.
      image.close()
      audio_clip.close()
      if Path('temp_art.png').is_file():
        Path('temp_art.png').unlink()
    
  
  def _final_render(self, clip: CompositeVideoClip, output_dir: str, filename: str):
    Path(output_dir).mkdir(exist_ok=True)
    clip.write_videofile(filename=f"{output_dir}/{filename}.mp4", fps=2, codec="libx264")

  def _valid_path(self, path: Path, regex: re, err: int) -> bool:
    if not regex.match(path.suffix):
      return False
    return True
  
  def _valid_audio(self, path: Path):
    audio_regex = re.compile("[.]wav$|[.]mp3$|[.]aiff?$|[.]ogg$|[.]flac")
    return self._valid_path(path, audio_regex, AUDIO_FILE_ERROR)

  def _valid_image(self, path: Path):
    image_regex = re.compile("[.]png$|[.]jpe?g$|[.]tiff$|[.]gif$")
    return self._valid_path(path, image_regex, IMAGE_FILE_ERROR)

  def get_image() -> int:
    return SUCCESS
  
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
    width, height = pi.size
    new_width = int(width * (1080/height))
    resize = pi.resize((new_width, 1080))
    resize.save('temp_art.png')
    return 'temp_art.png'
  
  def _create_image(self, current_audio: Path):
    tags = TinyTag.get(current_audio, image=True)
    color = self._hex_to_rgb(self.config.bg_color)
    image_bytes = tags.get_image()
    # Grabs image from directory.
    if self.image is not None:
      pi = Image.open(self.image)
      width, height = pi.size
      new_width = int(width * (1080/height))
      resize = pi.resize((new_width, 1080))
      resize.save('temp_art.png')
      image = ImageClip(resize)
      return image.on_color(size=(1920,1080), color=color)
    # Grabs image from metadata.
    elif image_bytes is not None:
      image_path = self._get_image_from_bytes(image_bytes)
      image = ImageClip(image_path)
      return image.on_color(size=(1920,1080), color=color)
    # Will eventually handle rendering without an image provided.
    
    text = TextClip(txt=f"{tags.artist}\n{tags.title}", font='Courier', color='white', size=(1920,1080))
    return text.on_color(size=(1920,1080), color=color)

  def _clean_string(self, string: str):
    return re.sub(r"\W", "", string)
