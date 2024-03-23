from pathlib import Path
from mp3_to_mp4.config import Config
from mp3_to_mp4.create_image import CreateImage
from mp3_to_mp4.utils import valid_audio_file, get_audio_list, get_cover_image_list, clean_string
from mp3_to_mp4.render import render
from mp3_to_mp4 import AUDIO_DIR_ERROR, SUCCESS, IMAGE_FILE_ERROR
from tinytag import TinyTag
from PIL import Image, ImageColor
from io import BytesIO

class Mp3ToMp4:
  def __init__(self, config: Config, audio: Path, image: Path, bg_image: Path, join: bool):
    self.config = config
    self.join = join
    self.audio = audio
    self.provided_image = image
    self.provided_bg_image = bg_image
    self.composite_image = None
    self._audio_list = []

  def render(self):
    if (err := self.get_audio()) != SUCCESS:
      return err
    if self.join:
      return self.__join_batch()
    return self.__render_batch()
  
  def __join_batch(self):
    tags = TinyTag.get(self._audio_list[0])
    self.get_image(self._audio_list[0])
    render(
      audio_list=self._audio_list,
      image=self.composite_image,
      filename=clean_string(f"{tags.album}"),
      output_path=self.config.output_path,
      join=True
    )

  def __render_batch(self):
    for audio in self._audio_list:
      self.get_image(audio)
      render(
        audio_list=[audio],
        image=self.composite_image,
        filename=audio.stem,
        output_path=self.config.output_path)

  
  def get_audio(self):
    # If the path is a valid audio file, proceed to return that to audio_list
    if self.audio.is_file() and valid_audio_file(self.audio):
      self._audio_list.append(self.audio)
    elif self.audio.is_dir():
    # If the path is a folder, proceed to get all the files on the folder and put on audio_list
      list = get_audio_list(self.audio)
      if list == 0:
        return AUDIO_DIR_ERROR
      self._audio_list = sorted(list, key=lambda path: path.name)
    return SUCCESS
  
  def get_image(self, audio: Path):
    # Goes through all relevant image config options to generate the image.
    img = CreateImage(
      dimensions=self.config.dimensions,
      color=ImageColor.getrgb(self.config.bg_color),
      font=str(self.config.font),
      font_scale=self.config.font_scale,
      font_color=ImageColor.getrgb(self.config.font_color),
      image_padding=self.config.image_padding,
      background_blur=self.config.background_blur,
      background_grow=self.config.background_grow,
      )
    tags = TinyTag.get(audio, image=True)
    
    if self.provided_image == None:
      if self.config.use_file_image:
        bytes = tags.get_image()
        if bytes != None:
          img.foreground = Image.open(BytesIO(bytes))
      if img.foreground == None and self.config.use_folder_image:
        if self.audio.is_dir():
          img.foreground = Image.open(get_cover_image_list(audio)[0])
        if self.audio.is_file():
          img.foreground = Image.open(get_cover_image_list(audio.parent)[0])
    else:
      img.foreground = Image.open(self.provided_image)
    # If a background image is provided, use that
    if self.provided_bg_image:
      img.background = self.provided_bg_image
    # If enable background image:
    elif self.config.enable_bg_image:
      img.background = img.foreground
      # Else use the cover image.
    if self.join:
      if tags.albumartist:
        img.text = f"{tags.albumartist}\n{tags.album}"
      else:
        img.text = f"{tags.artist}\n{tags.album}"
    else:
      img.text = f"{tags.artist}\n{tags.title}"
    self.composite_image = img.auto_image()
    if self.composite_image != None:
      return SUCCESS
    return IMAGE_FILE_ERROR
  
