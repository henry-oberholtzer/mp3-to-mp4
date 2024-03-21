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
  return f"tests/resources/LIBERATIONMONO-REGULAR.TTF"

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
    assert result.mode == "RGBA"
  def test_text_foreground(self, ci: CreateImage, font):
    ci.font = font
    ci.text = "Caroline Polachek\nSo Hot You're Hurting My Feelings"
    result = ci.text_foreground()
    assert result.size == ci.dimensions
  def test_resize_foreground(self, ci: CreateImage):
    ci.foreground = Image.new(mode="RGB", size=(600, 600), color=(0,0,0, 255))
    ci.dimensions = (300, 300)
    result = ci.resize_foreground()
    W, H = result.size
    assert (W, H) == ci.dimensions
  def test_resize_foreground_padding(self, ci: CreateImage):
    ci.foreground = Image.new(mode="RGBA", size=(600, 600), color=(0,0,0, 255))
    ci.dimensions = (300, 300)
    ci.image_padding = 25
    result = ci.resize_foreground()
    W, H = result.size
    assert (W, H) == (ci.dimensions[0] - 50, ci.dimensions[1] - 50)
  def test_image_background(self, ci: CreateImage):
    ci.background = Image.new(mode="RGBA", size=(800, 800), color=(0,0,0, 255))
    ci.background_blur = 0
    result = ci.image_background()
    assert result.size == (1920, 1080)
  def test_image_background_blur(self, ci: CreateImage):
    ci.background = Image.new(mode="RGBA", size=(800, 800), color=(0,0,0, 255))
    ci.background = Image.open("tests/resources/test_image.jpg")
    result = ci.image_background()
    assert result.size == (1920, 1080)
  def test_position_foreground(self, ci: CreateImage):
    # ci.foreground = Image.new(mode="RGB", size=(800, 800), color=(255, 128, 128))
    ci.foreground = Image.open("tests/resources/test_image.jpg")
    ci.image_padding = 100
    resize = ci.resize_foreground()
    assert resize.size == (880, 880)
    position = ci.position_foreground()
    assert position.size == (1920, 1080)
  def test_composite(self, ci: CreateImage):
    ci.foreground = Image.open("tests/resources/test_image.jpg")
    ci.background = Image.open("tests/resources/test_image.jpg")
    ci.image_padding = 100
    ci.resize_foreground()
    ci.position_foreground()
    ci.image_background()
    composite = ci.composite_image()
    assert composite.size == (1920, 1080)
  def test_composite(self, ci: CreateImage, font):
    ci.background = Image.open("tests/resources/test_image.jpg")
    ci.text = "Hypersurface\nHeaven And Earth"
    ci.font = font
    ci.font_color = (128, 0, 128)
    ci.text_foreground()
    ci.image_background()
    composite = ci.composite_image()
    assert composite.size == (1920, 1080)
