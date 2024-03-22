from pathlib import Path
from mp3_to_mp4.config import Config
from mp3_to_mp4.utils import valid_audio_file, get_audio_list
from mp3_to_mp4 import AUDIO_DIR_ERROR, SUCCESS
from tinytag import TinyTag

class Mp3ToMp4:
  def __init__(self, config: Config, audio: Path, image: Path, join: bool):
    self.config = config
    self.join = join
    self.audio = audio
    self.image = image
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
    if self.image == None:
      for audio in self._audio_list:
        pass
    return SUCCESS
