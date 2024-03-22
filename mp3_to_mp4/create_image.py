from PIL import Image, ImageFont, ImageDraw, ImageFilter
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
    image_padding: int = 0,
    background_blur: int = 10,
    background_grow: float = 0.5
    ):
    self.foreground = foreground
    self.background = background
    self.background_blur = background_blur
    self.background_grow = background_grow
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
    self.background.paste(self.foreground, (0,0), self.foreground)
    return self.background
    
  def solid_background(self):
    """
    Generates the background based on dimensions and color.
    """
    r,g,b = self.color
    img = Image.new(mode="RGBA", size=self.dimensions, color=(r,g,b,255))
    self.background = img
    return self.background
  
  def image_background(self):
    """
    Resizes & crops a provided image to serve as the background.
    
    Optional blur can be set.
    """
    W, H = self.background.size
    w, h = self.dimensions
    ratio = (w / W) * (1 + self.background_grow)
    scale = self.background.resize((int(H * ratio),int(W * ratio)), resample=Resampling.LANCZOS)
    s_w, s_h = scale.size
    side_margin = (s_w - w)/2
    vert_margin = (s_h - h)/2
    scale.putalpha(1)
    crop = scale.crop((side_margin, vert_margin, s_w - side_margin, s_h - vert_margin))
    if self.background_blur != 0:
      self.background = crop.filter(ImageFilter.GaussianBlur(radius = self.background_blur))
    else:
      self.background = crop
    return self.background
  
  def resize_foreground(self):
    """
    Resizes and positions a provided image to fit as the foreground image.
    """
    if self.foreground:
      W, H = self.foreground.size
      _, h = self.dimensions
      ratio = h / H
      new_w = int(W * ratio - (2*self.image_padding % W))
      new_h = int(h - (2*self.image_padding % h))
      self.foreground = self.foreground.resize((new_w, new_h), resample=Resampling.LANCZOS)
    return self.foreground
  
  def position_foreground(self):
    """
    Positions the foreground image on the center of the canvas, on a blank background.
    """
    img_w, img_h = self.foreground.size
    alpha = Image.new("RGBA", self.dimensions, (255, 255, 255, 0))
    bg_w, bg_h = alpha.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    alpha.paste(self.foreground, offset)
    self.foreground = alpha
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
