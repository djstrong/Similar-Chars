import Image, ImageDraw, ImageFont, math


class SimilarChars:
  letters = dict()
  similar = dict()
  threshold = 10
  
  def __init__(self, font, size):
    self.font = ImageFont.truetype(font, size)
    for i in xrange(32, 126):
      self.letters[i] = ImageComp(self.__letter_to_image(i, self.font))
      self.similar[i] = list()
  
  def compare(self):
    for i in xrange(1, 1220):
      im2 = ImageComp(self.__letter_to_image(i, self.font))
      for l,im in self.letters.iteritems():
	rms = self.__compare_images(im2, im)
	#print i, l, rms
	if rms<self.threshold and l!=i:
	  self.similar[l].append(i)
	  #print i, l, rms
  
  def print_similar(self):
    for l,i in self.similar.iteritems():
      if i:
	print l, i
  
  def print_similar_HTML(self):
    for l,i in self.similar.iteritems():
      if i:
	print unichr(l).encode('utf-8')+":"
	for i2 in i:
	  print unichr(i2).encode('utf-8')

  def print_similar_HTML2(self):
    for l,i in self.similar.iteritems():
      if i:
	print str(l)+'<img src="'+str(l)+'.png">'
	for i2 in i:
	  print str(i2)+'<img src="'+str(i2)+'.png">'
	print '<br>'
	  
  def __letter_to_image(self, letter, font):
    string = " "+unichr(letter) # some chars are not generating
    im = Image.new("L", (100, 100), 255) # "L" -greyscale
    draw = ImageDraw.Draw(im)
    im = im.crop((0,0)+draw.textsize(string, font=font))
    draw.text((0,0), string, fill="black", font=font)
    del draw
    #im.save(str(letter)+".png", "PNG")
    return im

    
  def __compare_images(self, im1, im2):
    width = min(im1.width, im2.width)
    height = min(im1.height, im2.height)
    mwidth = max(im1.width, im2.width)
    mheight = max(im1.height, im2.height)

    threshold2 = self.threshold**2 * mwidth * mheight # speed up

    rms = 0.0
    for i in xrange(width):
      for j in xrange(height):
	rms += (im1.pixel(i,j)-im2.pixel(i,j) )**2
      if rms >= threshold2:
	return self.threshold
	
    if im1.width>im2.width:
      bigger = im1
    else:
      bigger = im2
      
    for i in xrange(width, mwidth):
      for j in xrange(height):
	rms += (bigger.pixel(i,j)-255)**2 # 255 - white

    return math.sqrt(rms/mwidth/mheight)
    
class ImageComp:
  def __init__(self, im):
    self.data = tuple(im.getdata())
    self.width, self.height = im.size
  def pixel(self, x, y):
    return self.data[x + y*self.width]

sc = SimilarChars("DejaVuSerif.ttf", 20)
sc.compare()
#sc.print_similar()
#sc.print_similar_HTML()
sc.print_similar_HTML2()