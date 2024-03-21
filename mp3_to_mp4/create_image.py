from PIL import Image, ImageFont, ImageDraw
from PIL.Image import Resampling

class CreateImage:
  def __init__(self, 
    foreground: Image = None,
    background: Image = None,
    dimensions: tuple[int, int] = (1920, 1080),
    color: tuple[int,int,int] = (0, 0, 0),
    text: str = None,
    font: str = None,
    font_scale: float = 0.8,
    font_color: tuple[int, int, int] = (255, 255, 255),
    image_padding: int = 0
    ):
    self.foreground = foreground
    self.background = background
    self.dimensions = dimensions
    self.center = (int(dimensions[0]/2), int(dimensions[1]/2))
    self.color = color
    self.text = text
    self.font = font
    self.font_scale = font_scale
    self.font_color = font_color
    self.image_padding = image_padding
  
  def composite_image(self):
    """
    Composites the foreground and background properties into a single image.
    """
    
  def solid_background(self):
    """
    Generates the background based on dimensions and color.
    """
    img = Image.new(mode="RGB", size=self.dimensions, color=self.color)
    self.background = img
    return self.background
  
  def image_background(self):
    """
    Resizes & crops a provided image to serve as the background.
    
    Optional blur and opacity can be set.
    """
    return self.background
  
  def resize_foreground(self):
    """
    Resizes a provided image to fit as the foreground image.
    """
    if self.foreground:
      W, H = self.foreground.size
      _, h = self.dimensions
      ratio = h / H
      new_w = int(W * ratio - (2*self.image_padding % W))
      new_h = int(h - (2*self.image_padding % h))
      self.foreground = self.foreground.resize((new_w, new_h), resample=Resampling.LANCZOS)
    return self.foreground
  
  def text_foreground(self):
    """
    Generates foreground text based on provided text and font, scales to fit width.
    """
    text = Image.new("RGBA", self.dimensions, (255, 255, 255, 0))
    strings = sorted(self.text.split("\n"), key=lambda segment: len(segment))
    font_size = 1
    font = ImageFont.truetype(self.font, font_size)
    while font.getlength(strings[-1]) < self.font_scale*self.dimensions[0]:
      font_size += 1
      font = ImageFont.truetype(self.font, font_size)
    draw = ImageDraw.Draw(text)
    w, h = self.dimensions
    _, _, W, H = draw.textbbox((0, 0), self.text, font=font)
    draw.multiline_text(((w-W)/2, (h-H)/2), self.text, font=font, fill=self.font_color, align="center")
    self.foreground = text
    return self.foreground
