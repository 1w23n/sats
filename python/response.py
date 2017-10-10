#!/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

shell_name =
script_dir = os.getcwd()
common =

ip_list = [
    '192.168.254.224',
    '192.168.254.155',
    '192.168.254.172',
    '192.168.254.173',
    '192.168.254.174',
    '192.168.254.176',
    '192.168.254.177',
]

if common:
    os.
else:
    print('[ERROR] common function file not found.')
    os.

for host in ip_list:
    ping = subprocess.Popen(
            ['ping', '-w', '3', '-c', '1', host],
            subprocess.stdout.PIPE, subprocess.stderr.PIPE
           )
    out, err = ping.communicate()

    for line in out.split
      
    if 

