#!/usr/bin/python

import sys
import urllib

def wget(url):
  ufile = urllib.urlopen(url)  ## get file-like object for url
  info = ufile.info()   ## meta-info about the url content
  if info.gettype() == 'text/html':
    print 'base url:' + ufile.geturl()
    text = ufile.read()  ## read all its text
    # print text

def main():
  url = sys.argv[1]
  print url
  wget(url)

if __name__ == '__main__':
  main()
