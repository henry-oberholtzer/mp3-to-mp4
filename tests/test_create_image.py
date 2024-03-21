import pytest
import os
from pathlib import Path
from mp3_to_mp4.create_image import CreateImage
from PIL import Image

@pytest.fixture
def ci():
  return CreateImage()

@pytest.fixture
def font():
  return r"C:\development_projects\python\mp3-to-mp4\tests\resources\LIBERATIONMONO-REGULAR.TTF"

class TestCreateImage:
  def test_init(self):
    img = CreateImage()
    assert img.foreground == None
    assert img.foreground == None
    assert img.dimensions == (1920, 1080)
    assert img.center == (1920/2, 1080/2)
    assert img.color == (0,0,0)
    assert img.text == None
    assert img.font == None
    assert img.font_scale == 0.8
    assert img.font_color == (255, 255, 255)
    assert img.image_padding == 0
  def test_solid_background(self, ci: CreateImage):
    result = ci.solid_background()
    assert result.size == ci.dimensions
    assert result.mode == "RGB"
  def test_text_foreground(self, ci: CreateImage, font):
    ci.font = font
    ci.text = "Caroline Polachek\nSo Hot You're Hurting My Feelings"
    result = ci.text_foreground()
    assert result.size == ci.dimensions
  def test_resize_foreground(self, ci: CreateImage):
    ci.foreground = Image.new(mode="RGB", size=(600, 600), color=(0,0,0))
    ci.dimensions = (300, 300)
    result = ci.resize_foreground()
    W, H = result.size
    assert (W, H) == ci.dimensions
  def test_resize_foreground_padding(self, ci: CreateImage):
    ci.foreground = Image.new(mode="RGB", size=(600, 600), color=(0,0,0))
    ci.dimensions = (300, 300)
    ci.image_padding = 25
    result = ci.resize_foreground()
    W, H = result.size
    assert (W, H) == (ci.dimensions[0] - 50, ci.dimensions[1] - 50)
