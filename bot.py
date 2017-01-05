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
import sys
import youParse
import random

#channel = "#snucse17"
channel = "#pbzweihander"
server = "irc.uriirc.org"
port = 16664
nickname = "zweihander-bot"

flag = "\\"

irc = IRC()
irc.connect(server, port, channel, nickname)

joined_channels = [channel]
commands = {}
playlist = []

def main():
	commands.update({"quit": quit})
	commands.update({"reloadplist": getPlaylist})
	commands.update({"music": chooseMusic})
	commands.update({"join": join})
	commands.update({"part": part})
	getPlaylist("", [])

	while 1:
		text = irc.get_text()
		print(text)

		if "PRIVMSG" in text:
			chan = text.split("PRIVMSG ")[1].split()[0]
			if "#" not in chan:
				chan = text.split("!")[0][1:]
			if flag in text:
				msg = text.split(flag)[1]
				args = msg.split()
				func = commands.get(args[0])
				if func:
					arr = func(chan, args)
					if arr:
						if type(arr) is list or type(arr) is tuple:
							for m in arr:
								if m:
									irc.send(chan, m)
						else:
							irc.send(chan, m)

def quit(chan, args):
	irc.disconnect()
	sys.exit(0)

def getPlaylist(chan, args):
	global playlist
	playlist = youParse.crawl(
			"https://www.youtube.com/playlist?list=PL8fjrW04BOE7V9ZU3qXJ2nXF2uHkAUSeg")
	return "Playlist Reloaded",

def chooseMusic(chan, args):
	return random.choice(playlist),

def join(chan, args):
	global joined_channels
	if len(args) > 1:
		for c in args[1:]:
			if "#" in c:
				irc.join(c)
				joined_channels.append(c)
	else:
		return "Argument Error!"

def part(chan, args):
	if len(args) > 1:
		for c in args[1:]:
			irc.part(c)
	else:
		irc.part(chan)

main()

