#!/usr/bin/env python

"""

The format and emote tables are both processed once when the module is loaded.
To add new emotes to the EmoteHandler, use the add or setitem methods:

  e = EmoteHandler(emote_table)
  e[":-/"] = "some-face"
  e.add("some-face", ":-/ =-/") 

The setitem method is used to add additional operations to the FormatHandler.
The setitem handler requires a pre-compiled regular expression, and can take
a string with backreferences, or a function.

  f = FormatHandler(format_table)
  f[re.compile(inoculate("(^|\s)'([^']+)'(\s|$|.)"))] = "\\1<tt>\\2</tt>\\3"


This module will eventually use Gaim themes instead of hard-coded values
for the emotes.

Please note that match patterns must be inoculated if they contain special characters.
In session.py, the emote and format handlers operate on inoculated strings. It had to
be implemented that way, because inoculating after the emote/format transform would
cause the html generated by the transform to appear as plain text. This is really,
really problematic for regular expressions, because if you run the inoculate function
on a regular expression, it will probably screw it up. Regular expressions have to be
inoculated by hand.


"""

import re
from cixar.python.wrap import wrap
from cixar.ish.sh.inoculate import inoculate

EMOTE_URL = ".chat/art/tango"

emote_table = {
  "face-surprise":    ":-O :O 8-O",
  "face-wink":        ";) ;-)",
  "face-smile-big":   ":D :-D =D =-D",
  "face-smile":       ":) :-) =) =-)",
  "face-sad":         ":( :-( =( =-(",
  "face-plain":       ":| :-|",
  "face-glasses":     "8) 8-)",
  "face-devil":       inoculate(">:-D >:D >:-) >:)"),
  "face-crying":      ":'-( :'(",
  "face-angel":       "0:-) 0:)",
}

format_table = {
  "(^|\s)&lt;(https?://\S+) ([^>]+)&gt;(\s|$|.)": '\\1<a target="_blank" href="\\2">\\3</a>\\4',
  "(^|\s)([a-zA-Z1-10]+://\S+)(\s|$|\.)": '\\1<a target="_blank" href="\\2">\\2</a>\\3',
  "(^|\s)\*(\S[^*]+)\*(\s|$|\.)": "\\1<b>\\2</b>\\3",
  "(^|\s)_(\S[^_]+)_(\s|$|\.)": "\\1<u>\\2</u>\\3",
  "(^|\s)/(\S[^/]+)/(\s|$|\.)": "\\1<i>\\2</i>\\3",
  "(^|\s)'(\S[^']+)'(\s|$|\.)": "\\1<tt>\\2</tt>\\3",
}

class EmoteHandler(dict):
  def __init__(self, table):
    self.parse_table(table)

  def generate_image(self, emote):
    return '<img src="%s/%s.png" alt="%s" />' % (EMOTE_URL, self[emote], emote.replace('"', "'"))

  @wrap("".join)
  def transform(self, text):
    keys = sorted(self.keys(), key=len)
    
    while text:
      for emote in keys:
        if text.startswith(emote):
          yield self.generate_image(emote)
          text = text[len(emote):]
          break
      
      if len(text) > 0:
        yield text[0]
        text = text[1:]

  def add(self, img_name, patterns):
    for pattern in patterns.split():
      self[pattern] = img_name

  def parse_table(self, table):
    for img_name, patterns in table.items():
      self.add(img_name, patterns)

class FormatHandler(dict):
  def __init__(self, table):
    self.parse_table(table)

  def transform(self, text):
    for pattern, rep in self.items():
      text = pattern.sub(rep, text)
    
    return text

  def parse_table(self, table):
    for pattern, rep in table.items():
      self[re.compile(pattern)] = rep

if __name__ == '__main__':
  e = EmoteHandler(emote_table)
  f = FormatHandler(format_table)
  
  print e.transform("this ;-) is 0:-) a test :)")

  e[":-/"] = "some-face"
  print e.transform("Another test :-/")
  
  print f.transform("/this/ is *a test* and _this_ 'is another test'.")
  print f.transform("/this/ http://www.cixar.com/~segphault is *a test* and _this_ 'is another test'.")
  print e.transform(f.transform("And another: <http://www.cixar.com cixar> test :-)"))

  print f.transform("/test/ ftp://segphault@cixar.com:/home/segphault")
  print f.transform(inoculate("and another <http://www.cixar.com cixar> test"))
  print f.transform(inoculate("<https://www.cixar.com cixar>"))
  print f.transform("try *nick or* name to rename yourself.")

  f[re.compile("(^|\s)<\?py (.+) \?>(\s|$|.)")] = \
    lambda m: "".join([m.group(1), str(eval(m.group(2))), m.group(3)])

  print f.transform("this is a <?py (' '.join(str(x) for x in range(10))) ?> test")


