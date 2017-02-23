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

import socket
import ssl


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class IRC:
    irc = []

    def init(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc = ssl.wrap_socket(sock)

    def send(self, chan, msg):
        self.raw_send("PRIVMSG " + chan + " :" + msg)

    def raw_send(self, msg):
        self.irc.send(bytes(msg + "\r\n", "UTF-8"))
        print("[t] " + msg)

    def connect(self, server, port: int, channel, botnick):
        self.irc.connect((server, port))
        self.raw_send("USER " + botnick + " 0 * :zweihander-bot")
        self.raw_send("NICK " + botnick)
        self.raw_send("JOIN " + channel)

    def disconnect(self):
        self.raw_send("QUIT :bye!")

    def join(self, channel):
        self.raw_send("JOIN " + channel)

    def part(self, channel):
        self.raw_send("PART " + channel)

    def get_text(self):
        text = self.irc.recv(1024).decode("UTF-8", "ignore")
        lines = text.split("\n")
        return lines

    def op(self, chan, users):
        if len(users) > 4:
            uarr = chunks(users, 4)
            for arr in uarr:
                self.raw_send("MODE " + chan + " +" + ('o' * len(arr)) + " " + " ".join(arr))
        else:
            self.raw_send("MODE " + chan + " +" + ('o' * len(users)) + " " + " ".join(users))

    def deop(self, chan, users):
        if len(users) > 4:
            uarr = chunk(users, 4)
            for arr in uarr:
                self.raw_send("MODE " + chan + " -" + ('o' * len(arr)) + " " + " ".join(arr))
        else:
            self.raw_send("MODE " + chan + " -" + ('o' * len(users)) + " " + " ".join(users))
