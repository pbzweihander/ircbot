# Name: bot.py
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
# from sentence_generator import *
import sys
import youParse
import random
import time
# import pickle

channel = "#pbzweihander"
server = "irc.uriirc.org"
port = 16664
nickname = "zweihbot"

flag = ">"

admins = ["zweihander", "pbzweihander"]
commands = {}
playlist = []

irc = IRC()

# cfd = []

chimes = {}  # 맞장구 커맨드 리스트

beers = []  # 맥주 목록
last_beers = [] # 중복 방지용 목록
weekends = []   # 주말에 할 일 목록
last_weekends = []  # 중복 방지용
restaurants = []
last_restaurant = ""


def main():
    global irc, chimes

    while True:
        try:
            irc.init()
            irc.connect(server, port, channel, nickname)
        except:
            print("retrying connection..")
            time.sleep(1)
        break

    # 명령어 등록
    # commands.update({"disconnect": disconnect})
    # commands.update({"part": part})
    # commands.update({"command": cmd})
    commands.update({"join": join})
    commands.update({"음악목록갱신": get_playlist})
    commands.update({"맥주목록갱신": get_beerlist})
    commands.update({"주말목록갱신": get_weekendlist})
    # commands.update({"말뭉치갱신": get_cfd})
    commands.update({"맞장구갱신": get_chimelist})
    commands.update({"식당목록갱신": get_restaurantlist})
    commands.update({"선곡": choose_music})
    commands.update({"음악": choose_music})
    commands.update({"맥주": choose_beer})
    commands.update({"맥쥬": choose_beer})
    commands.update({"액체": choose_beer})
    commands.update({"주말": choose_weekend})
    commands.update({"점심": choose_lunch})
    commands.update({"저녁": choose_dinner})
    commands.update({"옵": give_op})
    # commands.update({"아무말": say_anything})
    get_playlist("", "", [])
    get_beerlist("", "", [])
    get_weekendlist("", "", [])
    # get_cfd("", "", [])
    get_chimelist("", "", [])
    get_restaurantlist("", "", [])

    while True:  # 메세지 받는 루프
        lines = irc.get_text()  # 받아온다

        for text in lines:
            if not text:
                continue

            if 'PING ' in text:  # 서버에서 핑 요청시 응답
                irc.raw_send('PONG ' + text.split()[1])

            if 'INVITE ' in text:  # 유저가 채널로 초대시 응답
                irc.join(text.split(':', 2)[-1])

            print("[r] " + text)  # 로그

            if 'PRIVMSG ' in text:  # 메세지
                chan = text.split("PRIVMSG ")[1].split()[0]
                sender = text.split("!")[0][1:]
                msg = text.split(":", 2)[2]

                if "#" not in chan:  # 채널 메세지가 아니라 쿼리(귓속말)
                    chan = sender

                if msg.strip() in chimes:  # 말장구 넣기
                    irc.send(chan, chimes.get(msg.strip()))

                if msg[0] == flag:  # 메세지 처리
                    args = msg.split()
                    if len(args) > 0:
                        func = commands.get(args[0][1:])
                        if func:
                            arr = func(chan, sender, args)
                            if arr:
                                for m in arr:
                                    if m:
                                        irc.send(chan, m)


def disconnect(chan, sender, args):  # 퇴장
    if sender in admins:
        irc.disconnect()
        time.sleep(0.5)
        sys.exit(0)
    else:
        return "접근 권한 거부 ._.",


def get_beerlist(chan, sender, args):  # 맥주 목록 갱신
    global beers
    beers = []
    with open('beers.list', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line:
                beers.append(line.strip())
    return "맥주 목록이 갱신됐어요 ><",


def choose_beer(chan, sender, args):
    global last_beers
    while True:
        b = random.choice(beers)
        if b not in last_beers:
            last_beers.append(b)
            if len(last_beers) > 5:
                last_beers = last_beers[1:]
            break
    return "당신을 위한 맥주 : %s" % b,


def get_weekendlist(chan, sender, args):
    global weekends
    weekends = []
    with open('weekend.list', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line:
                weekends.append(line.strip())
    return "주말 계획 목록이 갱신됐어요 ><",


def choose_weekend(chan, sender, args):
    global last_weekends
    while True:
        w = random.choice(weekends)
        if w not in last_weekends:
            last_weekends.append(w)
            if len(last_weekends) > 5:
                last_weekends = last_weekends[1:]
            break
    return "당신을 위한 주말 : %s" % w,


def get_playlist(chan, sender, args):  # 유투브 플레이리스트를 받아와 파싱해서 음악 목록을 얻어온다
    global playlist
    playlist = youParse.crawl(
        "https://www.youtube.com/playlist?list=PL8fjrW04BOE7V9ZU3qXJ2nXF2uHkAUSeg")
    if playlist:
        return "음악 목록이 갱신됐어요 ><",
    else:
        playlist = []
        return "갱신 중 에러 발생 ._.",


def get_cfd(chan, sender, args):  # 미리 저장된 CFD를 받아와 말뭉치를 갱신한다
    global cfd
    with open("cfd.pkl", 'rb') as f:
        cfd = pickle.load(f)
    if cfd:
        return "말뭉치가 갱신됐어요 ><",
    else:
        return "갱신 중 에러 발생 ._.",


def get_chimelist(chan, sender, args):
    global chimes
    with open("chime.list", 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line:
                before = line.split(':')[0].strip()
                after = line.split(':')[1].strip()
                chimes.update({before: after})
    return '맞장구 목록이 갱신됐어요 ><',


def choose_music(chan, sender, args):  # 선곡
    return random.choice(playlist),


def get_restaurantlist(chan, sender, args):
    global restaurants
    restaurants = []
    with open('restaurant.list', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line:
                restaurants.append(line.strip())
    return "식당 목록이 갱신됐어요 ><",


def choose_lunch(chan, sender, args):
    global last_restaurant
    while True:
        r = random.choice(restaurants)
        if r != last_restaurant:
            last_restaurant = r
            break
    return "!식단 점심 %s" % r,


def choose_dinner(chan, sender, args):
    global last_restaurant
    while True:
        r = random.choice(restaurants)
        if r != last_restaurant:
            last_restaurant = r
            break
    return "!식단 저녁 %s" % r,


def join(chan, sender, args):  # 채널 입장
    if sender in admins:
        if len(args) > 1:
            for c in args[1:]:
                if c[0] == "#":
                    irc.join(c)
                else:
                    irc.join("#" + c)
        else:
            return "명령이 잘못됐어요 ._.",
    else:
        return "접근 권한 거부 ._.",


def part(chan, sender, args):  # 채널 나가기
    if sender in admins:
        if len(args) > 1:
            for c in args[1:]:
                irc.part(c)
        else:
            irc.part(chan)
    else:
        return "접근 권한 거부 ._.",


def cmd(chan, sender, args):  # RAW 명령어 보내기
    if sender in admins:
        msg = " ".join(args[1:]) + "\r\n"
        irc.raw_send(msg)
    else:
        return "접근 권한 거부 ._.",


def give_op(chan, sender, args):  # 옵 주기
    if len(args) > 1:
        irc.op(chan, args[1:])
        return "옵 나눠드렸어요 ><",
    else:
        return "명령이 잘못됐어요 ._.",


def say_anything(chan, sender, args):  # 아무말 생성
    if not cfd:
        return "말뭉치 오류 ._.",
    if len(args) > 1:
        try:
            stc = generate_sentence(cfd, args[1])
        except ValueError:
            return "초기값이 잘못됐어요 ._.",
        return stc,
    else:
        return "명령이 잘못됐어요 ._.",


main()
