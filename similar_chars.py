#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Copyright (c) 2012, Krzysztof Wróbel <djstrong.dev@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
'''

import Image, ImageDraw, ImageFont
import math
import collections

class SimilarChars:
  """Looks for similar chars in specified font."""
  
  letters = dict()
  similar = collections.defaultdict(list)
  
  def __init__(self, font, size, numbers=range(32, 126), threshold=10.0, last_char=65535):
    """Load defined font.
    
    Args:
	font: A string representing path to font file.
	size: An integer representing size of font.
	numbers: A list of integers representing chars to compare with. Default range(32,126).
	threshold: A double representing threshold of similarity. Default 10.0.
	last_char: An integer representing last char to compare. Default 65535.
    """
    self.font_path = font
    self.font_size = size
    self.font = ImageFont.truetype(font, size)
    self.threshold = threshold
    self.last_char = last_char
    for i in numbers:
      self.letters[i] = ImageComp(self.__letter_to_image(i, self.font))
  
  def compare(self):
    """Starts comparison."""
    for i in xrange(1, self.last_char):
      im2 = ImageComp(self.__letter_to_image(i, self.font))
      for l,im in self.letters.iteritems():
	rms = self.__compare_images(im2, im)
	if rms<self.threshold and l!=i:
	  self.similar[l].append(i)

  def print_similar(self):
    """Prints results."""
    for l,i in self.similar.iteritems():
      if i:
	print l, i

  def print_similar_HTML(self):
    """Saves chars as images and prints HTML output with results."""
    print '''
<style type="text/css">
@font-face { 
  font-family: 'someFont';
  src: URL(\''''+self.font_path+'''\');
}
table {
  font-family: "someFont";
  font-size: '''+str(self.font_size)+'''px;
  border-collapse: collapse;
}
td {
  border-width: 1px;
  border-style: inset;
}
</style>
'''
    print '<table>'
    print '<tr><td>number</td><td>char</td><td>image</td><td>similar</td></tr>'
    for l,i in self.similar.iteritems():
      if i:
	self.__save_image(l)
	print '<tr><td>'+str(l)+'</td><td>'+' &#'+str(l)+';</td><td>'+' <img src="'+str(l)+'.png"></td>'
	print '<td><table>'
	for i2 in i:
	  self.__save_image(i2)
	  print '<tr><td>'+str(i2)+'</td><td>'+' &#'+str(i2)+';</td><td>'+' <img src="'+str(i2)+'.png"></td></tr>'
	print '</table></td></tr>'
    print '</table>'

  def __save_image(self, letter):
    """Saves char as image.
    
    Args:
      letter: An integer representing char.
    """
    im = self.__letter_to_image(letter, self.font)
    im.save(str(letter)+".png", "PNG")
    
  def __letter_to_image(self, letter, font):
    """Creates image with letter.
        
    Args:
      letter: An integer representing char.
      font: A Font instance.
    """
    string = " "+unichr(letter) # some chars are not generating
    im = Image.new("L", (100, 100), 255) # "L" -greyscale
    draw = ImageDraw.Draw(im)
    im = im.crop((0,0)+draw.textsize(string, font=font))
    draw.text((0,0), string, fill="black", font=font)
    del draw
    return im

    
  def __compare_images(self, im1, im2):
    """Compares two images using Root mean square.
    
    Args:
      im1: A first image.
      im2: A second image.
      """
    width = min(im1.width, im2.width)
    height = min(im1.height, im2.height)
    mwidth = max(im1.width, im2.width)
    mheight = max(im1.height, im2.height)

    threshold2 = self.threshold**2 * mwidth * mheight # speed up

    rms = 0.0
    for i in xrange(width):
      for j in xrange(height):
	if im1.pixel(i,j)!=im2.pixel(i,j):
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
  """Represents char as image."""
  def __init__(self, im):
    self.data = tuple(im.getdata())
    self.width, self.height = im.size
    
  def pixel(self, x, y):
    """Returns value of pixel on poosition (x,y)."""
    return self.data[x + y*self.width]


if __name__ == '__main__':
  sc = SimilarChars("DejaVuSerif.ttf", 20)
  sc.compare()
  #sc.print_similar()
  sc.print_similar_HTML()