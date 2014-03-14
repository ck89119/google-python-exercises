#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def my_key(url):
  return url[-8:-4]

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  match = re.search('_[\S]+', filename)
  if match:
    server_name = match.group()[1:]

  dict_urls = {}
  try:
    f = open(filename, 'rU')
    for line in f:
      match = re.search('GET [\S]+.jpg HTTP', line)
      if match:
        url = match.group()[4:-5] 
        if 'puzzle' in url:
          dict_urls['http://' + server_name + url] = 1
    f.close()
  except IOError:
    sys.stderr.write('problem reading:' + filename)
  
  urls = []
  for key in sorted(dict_urls.keys(), key=my_key):
    urls.append(key)
  return urls

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
  
  f = open(os.path.join(dest_dir, 'index.html'), 'w')
  f.write('<html><body>\n')
  
  i = 0
  for img_url in img_urls:
    print img_url
    filename = 'img%d' % i;
    if not os.path.exists(os.path.join(dest_dir, filename)):
      urllib.urlretrieve(img_url, os.path.join(dest_dir, filename))
    f.write('<img src="%s">' % filename)
    i += 1
  
  f.write('\n</body></html>\n')
  f.close()

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  print len(img_urls)
  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
