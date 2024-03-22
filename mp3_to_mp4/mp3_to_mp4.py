from pathlib import Path
from mp3_to_mp4.config import Config
from mp3_to_mp4 import SUCCESS

class Mp3ToMp4:
  def __init__(self, config: Config, audio: Path, image: Path, join: bool):
    self.config = config
    self.join = join
    self.audio = audio
    self.image = image
    
  def close(self):
    pass
  def render(self):
    pass
    # Create image
    # Create audio
    # Render video
  def build_audio(self):
    return SUCCESS
  def build_image(self):
    # Goes through all relevant image config options to generate the image.
    return SUCCESS
