""" Handles combining the audio and image into a final mp4 file"""
from pathlib import Path
import ffmpeg

class Render:
  def __init__(self, audio, image):
    self.audio = audio
    self.image = image
  def render(self, filename, output_path):
    return Path
