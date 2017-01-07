# Name: irc.py
# Author: pbzweihander
# Email: sd852456@naver.com
#
# Copyright (C) 2016-2017 pbzweihander
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

from irc import *
from sentence_generator import *
import sys
import youParse
import random
import time
import pickle

#channel = "#snucse17"
channel = "#pbzweihander"
server = "irc.uriirc.org"
port = 16664
nickname = "zweihbot"

flag = "\\"

admins = ["zweihander", "pbzweihander"]
commands = {}
playlist = []

irc = []

#doc = kolaw.open('constitution.txt').read()
cfd = []

def main():
    global irc

    while True:
        try:
            irc = IRC()
            irc.connect(server, port, channel, nickname)
        except:
            print("retrying connection..")
            time.sleep(1)
        break

    #commands.update({"quit": quit})
    commands.update({"join": join})
    #commands.update({"part": part})
    #commands.update({"command": cmd})
    commands.update({"음악목록갱신": get_playlist})
    commands.update({"말뭉치갱신": get_cfd})
    commands.update({"선곡": choose_music})
    commands.update({"음악": choose_music})
    commands.update({"옵": give_op})
    commands.update({"아무말": say_anything})
    get_playlist("", "", [])
    get_cfd("", "", [])

    while True:
        lines = irc.get_text()
        
        for text in lines:
            if not text:
                continue
            if 'PING ' in text:
                irc.raw_send('PONG ' + text.split()[1])
            if 'INVITE ' in text:
                irc.join(text.split(':', 2)[-1])
            print("[r] " + text)
            if 'PRIVMSG ' in text:
                chan = text.split("PRIVMSG ")[1].split()[0]
                sender = text.split("!")[0][1:]
                msg = text.split(":", 2)[2]
                if "#" not in chan:
                    chan = sender
                if msg[0] == flag:
                    args = msg.split()
                    if len(args) > 0:
                        func = commands.get(args[0][1:])
                        if func:
                            arr = func(chan, sender, args)
                            if arr:
                                if type(arr) is list or type(arr) is tuple:
                                    for m in arr:
                                        if m:
                                            irc.send(chan, m)
                                else:
                                    irc.send(chan, arr)
                else:
                    with open("/home/pi/projects/python/ircbot/log.txt", 'w') as f:
                        f.write(msg + "\n")

def quit(chan, sender, args):
    if sender in admins:
        irc.disconnect()
        time.sleep(0.5)
        sys.exit(0)
    else:
        return "접근 권한 거부 ._."

def get_playlist(chan, sender, args):
    global playlist
    playlist = youParse.crawl(
            "https://www.youtube.com/playlist?list=PL8fjrW04BOE7V9ZU3qXJ2nXF2uHkAUSeg")
    if playlist:
        return "음악 목록이 갱신됐어요 ><",
    else:
        playlist = []
        return "갱신 중 에러 발생 ._.", 

def get_cfd(chan, sender, args):
    global cfd
    with open("cfd.pkl", 'rb') as f:
        cfd = pickle.load(f)
    if cfd:
        return "말뭉치가 갱신됐어요 ><",
    else:
        return "갱신 중 에러 발생 ._.",

def choose_music(chan, sender, args):
    return random.choice(playlist),

def join(chan, sender, args):
    global joined_channels
    if sender in admins:
        if len(args) > 1:
            for c in args[1:]:
                if c[0] == "#":
                    irc.join(c)
                else:
                    irc.join("#" + c)
        else:
            return "명령이 잘못됐어요 ._."
    else:
        return "접근 권한 거부 ._."

def part(chan, sender, args):
    if sender in admins:
        if len(args) > 1:
            for c in args[1:]:
                irc.part(c)
        else:
            irc.part(chan)
    else:
        return "접근 권한 거부 ._."

def cmd(chan, sender, args):
    if sender in admins:
        msg = " ".join(args[1:]) + "\r\n"
        irc.raw_send(msg)
    else:
        return "접근 권한 거부 ._."

def give_op(chan, sender, args):
    if len(args) > 1:
        irc.op(chan, args[1:])
        return "옵 나눠드렸어요 ><"
    else:
        return "명령이 잘못됐어요 ._."

def say_anything(chan, sender, args):
    if not cfd:
        return "말뭉치 오류 ._."
    if len(args) > 1:
        try:
            stc = generate_sentence(cfd, args[1])
        except ValueError:
            return "초기값이 잘못됐어요 ._."
        return stc
    else:
        return "명령이 잘못됐어요 ._."


main()

