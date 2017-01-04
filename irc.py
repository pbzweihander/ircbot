# Name: irc.py
# Author: pbzweihander
# Email: sd852456@naver.com
# 
# Copyright (C) 2016-2017 pbzweihander
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import socket
import ssl

class IRC:
	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc = ssl.wrap_socket(sock)
	
	def send(self, chan, msg):
		self.irc.send(bytes("PRIVMSG " + chan + " :" + msg + "\r\n", "UTF-8"))

	def rawsend(self, msg):
		self.irc.send(bytes(msg, "UTF-8"))

	def connect(self, server, port : int, channel, botnick):
		self.irc.connect((server, port))
		self.rawsend("USER " + botnick + " 0 * :zweihander-bot\r\n")
		self.rawsend("NICK " + botnick + "\r\n")
		self.rawsend("JOIN " + channel + "\r\n")
	
	def disconnect(self):
		self.rawsend("QUIT :bye!")

	def join(self, channel):
		self.rawsend("JOIN " + channel + "\r\n")

	def part(self, channel):
		self.rawsend("PART " + channel + "\r\n")

	def get_text(self):
		rawtext = self.irc.recv(1024)
		#print(rawtext)
		text = rawtext.decode("UTF-8")

		if text.find('PING') != -1:
			self.rawsend('PONG ' + text.split()[1] + '\r\n')

		return text


