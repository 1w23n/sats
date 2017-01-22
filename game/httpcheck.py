#!/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError

url = "https://foo.bar.baz.tv/"

html = ""
html_check = ""
comment = "# " + "-" * 70

uri_list = [
  "aaa", "bbb", "ccc", "ddd", "eee", "fff", "ggg",
  "hhh", "iii", "jjj", "kkk", "lll", "mmm", "nnn",
  "ooo", "ppp", "qqq", "rrr", "sss", "ttt", "uuu",
  "vvv", "www", "xxx", "yyy", "zzz",
]

if __name__ == '__main__':

  for uri in issuer_list:

    fullurl = url + uri + "/"

    try:
      result = urlopen(fullurl)

      print("# ---", uri, "--- #")
      print(result.geturl())
      print("Reason:", result.reason, "\n")
      print(result.headers)

      html = html + "\n" + "# --- " + uri + " --- #"

      for line in result.readlines():
        html = html + line.decode('shift_JIS')

      if (result.code == 200):
        html_check = html_check + "?!: " + uri + "\n"

    except (HTTPError) as page:
      print("# ---", uri, "--- #")
      print(page.geturl())
      print("ErrorCode:", page.code)
      print("Reason:", page.reason, "\n")
      print(page.headers)

      if (page.code == 404):
        html_check = html_check + "OK: " + uri + "\n"
      elif (page.code == 500):
        html_check = html_check + "NG: " + uri + "\n"
      else:
        html_check = html_check + "?!: " + uri + "\n"

  print(comment + "\n" + "# All HTML page result" + "\n" + comment)
  print(html)

  print(comment + "\n" + "# HTTP transaction result" + "\n" + comment)
  print(html_check)
