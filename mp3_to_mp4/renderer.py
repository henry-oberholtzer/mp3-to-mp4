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

from mp3_to_mp4 import (__app_name__, SUCCESS, AUDIO_FILE_ERROR, config)

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
      return self._close_render(self, image, audio)
  
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
    return self._close_render(image, audio_compile)
  
  
  def _close_render(self, image, audio):
    image.close()
    audio.close()
    if Path('temp_art.png').is_file():
        Path('temp_art.png').unlink()
    return SUCCESS
  
  def _final_render(self, clip: CompositeVideoClip, output_dir: str, filename: str):
    Path(output_dir).mkdir(exist_ok=True)
    clip.write_videofile(filename=f"{output_dir}\\{filename}.mp4", fps=self.config.output_fps, codec="libx264", audio_bitrate="320k", ffmpeg_params=['-tune','stillimage'])

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
    directory = self.path.glob("*.*")
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
  
  def _image_scale_dimensions(self, dimensions: tuple[int, int]) -> tuple:
    w, h = dimensions
    new_width = int(w * (self.config.height/h)) - (2*self.config.image_padding % w)
    new_height = int(self.config.height - (2*self.config.image_padding % h))
    return (new_width, new_height)
  
  def _image_hex_to_rgb(self, hex: str) -> tuple:
    h = hex.lstrip("#")
    if len(h) == 3:
      return tuple(int(h[i] + h[i], 16) for i in (0, 1, 2))
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
  
  def _image_resize(self, img):
    i = Image.open(img)
    return i.resize(self._image_scale_dimensions(i.size), resample=Resampling.LANCZOS)
  
  def _image_clip_on_color(self, img, filepath) -> ImageClip:
    color = self._image_hex_to_rgb(self.config.bg_color)
    resize = self._image_resize(img)
    resize.save(filepath)
    image = ImageClip(filepath)
    return image.on_color(size=self.dimensions, color=color)
  
  def _image_text_on_color(self, tags) -> ImageClip:
    color = self._image_hex_to_rgb(self.config.bg_color)
    text = TextClip(txt=f"{tags.artist}\n{tags.title}", font='Courier', color='white', size=self.dimensions)
    if self.join:
      text = TextClip(txt=f"{tags.albumartist}\n{tags.album}", font='Courier', color='white', size=self.dimensions)
    return text.on_color(size=self.dimensions, color=color)
  
  def _create_image(self, current_audio: Path) -> ImageClip:
    tags = TinyTag.get(current_audio, image=True)
    filename = Path("temp_art.png")
  # Grabs image from directory.
    if self.image is not None:
      return self._image_clip_on_color(self.image, filepath=filename)
  # Grabs image from metadata.
    elif (image_bytes := tags.get_image()) is not None:
      return self._image_clip_on_color(io.BytesIO(image_bytes), filepath=filename)
  # Will eventually handle rendering without an image provided.
    elif (folder_image := self._find_image_in_folder()) is not None:
      return self._image_clip_on_color(folder_image, filepath=filename)
    else:
      return self._image_text_on_color(tags)

  
