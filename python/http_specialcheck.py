#!/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import socket
from threading import Thread, Lock
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

pa_log = "html_collect.log_{0:%Y%m%d}".format(datetime.datetime.now())
collect = ""
timeout = 3
socket.setdefaulttimeout(timeout)

url = "https://hage.huge.hoge/"

uri_list = [
    "foo", "bar", "baz",
    "foobar", "foobarbaz",
]


class httpThread(Thread):

    def __init__(self, uri):
        Thread.__init__(self)
        self.uri = uri

    def run(self):
        global collect
        global lock
        fullurl = url + self.uri + "/"

        try:
            req = Request(fullurl)
            res = urlopen(fullurl)

            for line in res.readlines():
                print(html + line.decode('shift_JIS'))
            if (res.code == 200):
                print("?!: " + self.uri)

        except (HTTPError) as page:
            lock.acquire()
            collect += "# ---" + self.uri + "--- #" + "\n"
            collect += page.geturl() + "\n"
            collect += "ErrorCode: " + str(page.code) + "\n"
            collect += "Reason: " + page.reason + "\n"
            collect += str(page.headers)
            lock.release()

            if (page.code == 404):
                judge = page.headers
                if (judge.get_content_type() == "text/html"):
                    print("Renew: " + self.uri)
                else:
                    print("Corrently: " + self.uri)
            elif (page.code == 500):
                print("NG: " + self.uri)
            else:
                print("?!: " + self.uri)

        except (URLError) as page:
            print("Timeout: URL failure or Network/Server down.(" + fullurl + ")")
            collect += "# ---" + fullurl + "--- #" + "\n"
            collect += "Date: " + \
                str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))
            collect += "\nReason: " + str(page.reason) + "\n\n"

if __name__ == '__main__':
    lock = Lock()
    start_time = time.time()

    for i in uri_list:
        getting = httpThread(i)
        getting.start()
    getting.join()

    end_time = time.time() - start_time

    time.sleep(2)
    print("procesing time: " + str(end_time) + "[sec]")

    with open(pa_log, "a") as w:
        w.write(collect)
