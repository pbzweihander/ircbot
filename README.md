zweihander-bot
========
[pbzweihander]의 IRC 봇

```console
# 음악 추천 기능
>음악
>선곡
# 맥주 추천 기능
>맥주
# channel operator 주기
>옵 <닉네임1> <닉네임2> ...
# 랜덤 문장 생성
>아무말 <초기값>
```

<br>

Getting Started
--------

### prerequisites
- Python ≥ *3.5*
- [KoNLPy](https://github.com/konlpy/konlpy) (with MeCab)
- [NLTK](http://www.nltk.org/)

### Installation
```bash
vim bot.py
    # edit bot.py file to change server URL, port number, admin list,
    # and directory path
vim zweihbot.service
    # edit .service file to fit your path
sudo cp zweihbot.service /etc/systemd/system
sudo systemctl daemon-reload

sudo systemctl enable zweihbot
sudo systemctl start zweihbot
```

<br>

--------

[GNU AGPL 3.0 License](LICENSE.md)

[pbzweihander]: https://github.com/pbzweihander
