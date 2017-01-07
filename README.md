zweihander-bot
========
[pbzweihander]의 IRC 봇

```console
# 음악 추천 기능
\음악
\선곡
# channel operator 주기
\옵 <닉네임1> <닉네임2> ...
# 랜덤 문장 생성
\아무말 <초기값>
```

<br>

Getting Started
--------

### prerequisites
- Python ≥ *3.5*
- KoNLPy (with MeCab)
- NLTK

### Installation
```bash
sudo cp zweihbot.service /etc/systemd/system
sudo systemctl daemon-reload

sudo systemctl enable hyeonbot
sudo systemctl start hyeonbot
```

<br>

--------

[GNU AGPL 3.0 License](LICENSE.md)

[pbzweihander]: https://github.com/pbzweihander
