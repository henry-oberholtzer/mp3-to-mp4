from pathlib import Path
from mp3_to_mp4.config import Config
from mp3_to_mp4.utils import valid_audio_file, get_audio_list, get_cover_image_list
from mp3_to_mp4 import AUDIO_DIR_ERROR, SUCCESS
from tinytag import TinyTag
from PIL import Image
from io import BytesIO

class Mp3ToMp4:
  def __init__(self, config: Config, audio: Path, image: Path, bg_image: Path, join: bool):
    self.config = config
    self.join = join
    self.audio = audio
    self.image = image
    self.bg_image = bg_image
    self._audio_list = []

  def render(self):
    self.get_audio()
    self.get_image()
    self.build_video()
    self.close()

  def close(self):
    pass
  
  def build_video(self):
    pass
  
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
      # Then combine the audio files if join is true, and replace audio list with that.
      # call in the render function to concat all the audio in the list.
    return SUCCESS
  
  def get_image(self):
    # Goes through all relevant image config options to generate the image.
    if self.image == None and self.config.use_file_image:
      bytes = TinyTag.get(self._audio_list[0], image=True).get_image()
      if bytes != None:
        self.image = Image.open(BytesIO(bytes))
    if self.image == None and self.config.use_folder_image:
      if self.audio.is_dir():
        self.image == Image.open(get_cover_image_list(self.audio)[0])
      if self.audio.is_file():
        self.image == Image.open(get_cover_image_list(self.audio.parent)[0])
    if self.image == None:
      # Make an image with text.
      pass
    # If enable background image:
      # If a background image is provided, use that
      # Else use the cover image.
    # Else
      # Position image or text on a background.
    return SUCCESS
